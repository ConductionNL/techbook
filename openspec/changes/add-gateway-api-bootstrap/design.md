# Design: add-gateway-api-bootstrap

Dit document draagt de besluiten. De change zelf is de audit-trail — er is in
deze vloot geen aparte ADR-conventie voor cluster-repo's. Dat is relevant voor
NEN-EN-ISO/IEC 27001:2023 Annex A.8.9 (Configuration management): niet alleen
de uitkomst maar ook de afweging moet later herleidbaar zijn.

## Besluit 1 — doelrepo is cluster-infra, niet een nieuwe repo

Onderzocht op 2026-08-17, in deze volgorde:

1. **Bestaat er al een repo voor cluster-scoped platform-add-ons onder Argo?**
   Ja. `cluster-infra` bevat één `AppProject` en acht Applications
   (`argocd`, `external-dns`, `cert-manager-config`, `external-secrets`,
   `reflector`, `fuse-device-plugin`, `seccomp-profiles`, `storage`), platte
   structuur, één Application per component, geen app-of-apps en geen
   ApplicationSet.
2. **Wordt die repo herstructureerd?** Nee. De layout wordt actief afgedwongen
   door `scripts/verify.sh` (doc-assertie op `docs/index.md`) en beschreven in
   `README.md` en `docs/agents.md`. De enige openstaande "waar hoort dit"-vraag
   in de vloot is `add-portal-access-split`, en die gaat over een ander
   onderwerp.
3. **Is greenfield te rechtvaardigen?** Nee. Sterker: de plek was al
   voorbereid — `argo/projects/cluster-infra.yaml` bevat sinds langer
   `# ingress-nginx (future)` in `sourceRepos` en `namespace: ingress-nginx`
   in `destinations`. De ingress-laag hoorde hier al thuis.

`cluster-config` viel af: dat is een spoor-1 bash-scriptsrepo zonder
Argo-manifests, en staat bovendien zelf op een feature-branch met ongecommit
werk.

Consequentie voor de vorm: Application-per-component, multi-source
`$values`-patroon voor Helm (zoals `external-dns`), `ServerSideApply=true` voor
grote CRD's (zoals `external-secrets` en `argocd`), en een rij in
`docs/index.md` want anders faalt `verify.sh`.

## Besluit 2 — CRD's vendoren, en wat de chart levert, niet het standard channel

Drie opties gewogen:

| | CRD-tekst staat in | Nadeel |
|---|---|---|
| chart bezit ze (`crds.enabled=true`) | docker.io | niet in git; bump verandert CRD's stilzwijgend mee |
| aparte Application naar `kubernetes-sigs/gateway-api` | GitHub | live afhankelijkheid bij elke sync; versie kan uit de pas lopen met de chart |
| **vendoren in cluster-infra** | deze repo | ~3,6 MB YAML; bump is handwerk |

Gekozen: vendoren. Volgt het `argocd`-precedent in dezelfde repo (bewust
hermetisch in plaats van een remote base) en de regel na het OLM-incident van
2026-08-10: neem het release-artefact, geen live verwijzing.

Daarbinnen een tweede keuze die minder vanzelfsprekend is. Het upstream
release-asset `standard-install.yaml` van Gateway API v1.5.1 bevat **8** CRD's.
De chart installeert er **12** — daarbovenop `tcproutes`, `udproutes` en twee
experimentele `gateway.networking.x-k8s.io`-types. De ClusterRole van Envoy
Gateway watcht `tcproutes`, `udproutes`, `tlsroutes`, `grpcroutes`,
`listenersets` en `backendtlspolicies`. Met alleen het standard-channel-bestand
start de controller die informers niet.

Gevendord is daarom de gerenderde CRD-subchart van de gepinde chart:

    helm template crds <chart>/charts/crds --include-crds

Eén bestand, één commando, en verifiëren is een `diff`. Dat is sterkere
herkomst dan een met de hand samengesteld bestand.

`prune: false` op die Application. Een CRD verwijderen wist in één keer élk
object van dat type — alle Gateways en HTTPRoutes tegelijk. Dat moet een
aparte, bewuste handeling van een mens zijn.

## Besluit 3 — PROXY-protocol is een voorwaarde, geen optimalisatie

Gemeten op de bestaande Service `nginx-ingress-nginx-controller`:

    loadbalancer.openstack.org/proxy-protocol: "true"
    loadbalancer.openstack.org/timeout-client-data: "600000"

en `use-proxy-protocol: true` in de controller-ConfigMap.

De OpenStack-LB stuurt dus een PROXY-header. Envoy sluit een verbinding waarvan
hij die header niet verwacht. Zonder `ClientTrafficPolicy` komt er geen enkel
pakket door — geen degradatie, maar niets. De Service-annotaties (via
`EnvoyProxy`) en de policy horen bij elkaar en mogen nooit los gewijzigd worden.

`optional: false`: verkeer zonder PROXY-header wordt geweigerd. De enige weg
naar deze listeners loopt via de LB; op `true` zetten zou het clientadres
vervalsbaar maken.

Geen `clientIPDetection.xForwardedFor`. Met PROXY-protocol kent Envoy het echte
clientadres al en zet hij dat zelf in X-Forwarded-For. Een binnenkomende
XFF-header vertrouwen zou juist het gat openen dat de nginx-annotaties
`use-forwarded-headers` / `enable-real-ip` / `compute-full-forwarded-for`
vandaag dichthouden.

## Besluit 4 — geen DNS-cutover voor de Nextcloud-canary

`nextcloud-canary-accept-tls` wordt via HTTP-01 vernieuwd, en die challenge
loopt over de nginx-Ingress. Zodra de host naar Envoy wijst, breekt de
vernieuwing — stil, en pas zichtbaar bij de eerstvolgende renewal.

cert-manager v1.18.0 heeft Gateway API-ondersteuning op GA, maar de vlag
`--enable-gateway-api` staat niet op de deployment (gecontroleerd 2026-08-17).
Aanzetten vereist dat de CRD's er eerst zijn, anders start de controller niet.

Daarom: de Nextcloud-canary valideren met `curl --resolve` tegen het Envoy-IP,
zonder DNS aan te raken. Een echte cutover is een vervolgstap ná het aanzetten
van die vlag. De twee WOO-frontends hebben dit probleem niet — die hangen aan
het DNS-01-wildcard.

## Besluit 5 — filters afgeleid van gemeten headers, niet van annotaties

De vertaling van nginx-annotaties naar HTTPRoute-filters is opgesteld uit wat er
op de lijn staat (`curl -I https://canary.accept.commonground.nu/status.php`,
2026-08-17), niet uit `Nextcloud-base/values/common.yaml`. Dat scheelde twee
fouten:

- `nginx.ingress.kubernetes.io/hsts-max-age` is geen geldige annotatie maar een
  ConfigMap-instelling. De `15552000` in `common.yaml` doet niets; op de lijn
  staat de controller-default `31536000`.
- De nginx-sidecar in de pod zet zelf ook een HSTS-header (`15768000`), maar
  die haalt de client niet — ingress-nginx overschrijft hem.

De CORS-instelling is overgenomen zoals hij is, niet zoals hij bedoeld lijkt:
`allow-origin: *` samen met `allow-credentials: true` wordt door elke browser
geweigerd, en `allow-headers` is teruggebracht tot alleen `X-Forwarded-For`.
Dat repareren hoort niet in een migratie die pariteit moet aantonen. Apart
gemeld.

## Wat deze change bewust NIET oplost

`allowedRoutes.namespaces.from: All` is even permissief als de huidige
Ingress-situatie. De multi-tenant-isolatie die de aanleiding vormt, wordt door
deze change dus *mogelijk gemaakt* maar niet *gerealiseerd*. Dat is een
expliciete keuze: het isolatiemodel vaststellen is een apart gesprek, en het
tegelijk doen zou de canary onvergelijkbaar maken met de Ingress ernaast.
