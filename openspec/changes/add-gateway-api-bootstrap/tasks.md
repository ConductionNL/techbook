# Tasks: add-gateway-api-bootstrap

## 1. Akkoord

- [ ] 1.1 MENS: AKKOORD (Mark, <datum>) — de proposal, en met name de
      tweede OpenStack-loadbalancer (eigen publiek IP, kostenpost,
      firewallregel) en de vier tijdelijke Applications

## 2. Inventarisatie (read-only) — afgerond

- [x] 2.1 Live staat van de ingress-laag meten — 2026-08-17: controller
      v1.12.2 (niet 1.12.3), `allow-snippet-annotations: true` +
      `annotations-risk-level: Critical`, 236 Ingresses waarvan 233 op
      class `nginx`, 118 met `enable-cors`, 34 met een per-ingress
      `server-snippet`
- [x] 2.2 Herkomst van de webfinger/CalDAV-set herleiden — 2026-08-17:
      staat globaal in de controller-ConfigMap en in de nginx-sidecar
      in de pod, NIET op de tenant-Ingresses. De 34 per-ingress
      snippets horen bij de legacy Helm-tenants en bevatten alleen
      `server_tokens off` + `proxy_hide_header`. Gevolg: er valt op
      ingress-niveau niets te vertalen naar `URLRewrite`-filters
- [x] 2.3 Doelrepo bepalen en onderbouwen — 2026-08-17: cluster-infra,
      zie design.md besluit 1. Plek was al voorbereid in het AppProject
- [x] 2.4 Versies vaststellen — 2026-08-17: Envoy Gateway 1.8.3
      (bundelt Gateway API v1.5.1, vereist k8s >= 1.32; cluster draait
      v1.35). De v1.2-pin uit het oorspronkelijke voorstel vervalt
- [x] 2.5 cert-manager-compatibiliteit — 2026-08-17: v1.18.0, Gateway
      API-ondersteuning is GA maar `--enable-gateway-api` staat niet op
      de deployment. Niet blokkerend voor de canary's (wildcard +
      ReferenceGrant), wél voor een echte DNS-cutover
- [x] 2.6 Canary-kandidaten selecteren — 2026-08-17: op
      `tenant.wave: "0"` + `environment: accept`, want een tenant
      zonder CORS-annotatie bestaat niet. Gekozen:
      `canary-accept/woo-website`, `almere-accept/woo-website`,
      `canary-accept/nextcloud`

## 3. Vastleggen in cluster-infra — afgerond, wacht op review

- [x] 3.1 CRD's vendoren uit de gepinde chart — 2026-08-17:
      `gateway-api/crds/envoy-gateway-crds-1.8.3.yaml` (20 CRD's +
      safe-upgrade-policy, 3,6 MB), herkomst en bump-procedure in
      `gateway-api/README.md`. AFWIJKING van het oorspronkelijke
      voorstel: niet het standard-channel-asset (8 CRD's) maar wat de
      chart levert (12), omdat Envoy Gateway `tcproutes`/`udproutes`/
      `listenersets` watcht — zie design.md besluit 2
- [x] 3.2 Vier Applications — 2026-08-17: `gateway-api-crds`
      (`prune: false`), `envoy-gateway` (chart 1.8.3,
      `crds.enabled=false`), `envoy-gateway-config`,
      `gateway-canary-routes`
- [x] 3.3 AppProject uitbreiden — 2026-08-17: OCI-bron
      `docker.io/envoyproxy`, destination `envoy-gateway-system`, twee
      met naam genoemde canary-namespaces (geen wildcard), en de
      cluster-scoped types `GatewayClass` en
      `ValidatingAdmissionPolicy(Binding)`
- [x] 3.4 `external-dns` leest `gateway-httproute` — 2026-08-17:
      additief; geverifieerd dat de chart de ClusterRole zelf uitbreidt
- [x] 3.5 Reflector-regex op het openwoo-wildcard uitgebreid met
      `envoy-gateway-system` — 2026-08-17
- [x] 3.6 Docs + gates — 2026-08-17: `docs/gateway-api.md`, rijen in
      `docs/index.md`, README bijgewerkt, `verify.sh` valideert
      `envoy-gateway/` mee. `./scripts/verify.sh` groen, pre-commit
      pre-push groen
- [ ] 3.7 MENS: review + merge van de wijziging in cluster-infra

## 4. Bootstrap (mens doet elke cluster-actie) — afgerond 2026-08-17

Volgorde is niet vrij: elke stap `Synced Healthy` voor de volgende.

- [x] 4.0 `kubectl apply -f argo/projects/cluster-infra.yaml` — ONTBRAK in de
      eerste runbook. Het AppProject wordt door geen enkele Application
      beheerd; zonder deze apply worden alle andere geweigerd
- [x] 4.1 `gateway-api-crds` — Synced Healthy, 20 CRD's in het cluster
- [x] 4.2 `envoy-gateway` — Synced Healthy. De OCI-pull van
      `docker.io/envoyproxy` zonder `oci://`-prefix werkt
- [x] 4.3 `envoy-gateway-config` — Synced, dataplane-pod 2/2
- [x] 4.4 LoadBalancer kreeg **81.24.11.239**; Gateway `Programmed=True`
- [x] 4.5 Canary-routes uitgerold — 2026-08-17. Tijdelijk via een eigen
      Application; in fase 6 vervangen door de generators

**Incident tijdens deze fase.** De `--source=gateway-httproute`-wijziging
van external-dns zat in dezelfde commit als de rest en landde dus vóór de
CRD's. Gevolg: external-dns crashloopte op
`failed to sync *v1beta1.Gateway: context deadline exceeded`. Geen DNS-schade
— hij stopt vóór de reconcile-loop — en hersteld zodra 4.1 klaar was. De
proposal schreef een aparte commit met een eigen sync-moment voor; dat is niet
gevolgd. Staat als waarschuwing in `cluster-infra/docs/gateway-api.md`.

## 5. Canary valideren — grotendeels afgerond 2026-08-17

- [x] 5.1 Nextcloud via `--resolve` tegen `81.24.11.239`: `status.php`
      200, `.well-known/caldav` 301, `config/config.php` 404
- [x] 5.2 Poort 80 geeft 308, exact als nginx
- [x] 5.3 HSTS identiek: `max-age=31536000; includeSubDomains`
- [x] 5.4 **Vier gemeten verschillen**, geen ervan een regressie, alle
      vier vastgelegd in `cluster-infra/docs/gateway-api.md`:
      webfinger 301 vs 404 (nginx herschrijft intern via de globale
      ConfigMap-snippet); `config/config.php` 404 vs 403 (sidecar vs
      ingress-niveau, beide dicht); CORS-headers op een gewone GET
      alleen bij nginx; preflight echoot bij Envoy de Origin in plaats
      van `*` — wat mét `allow-credentials: true` juist wél bruikbaar is
- [x] 5.5 **DNS is niet verschoven.** Beide frontend-hosts wijzen nog
      naar `81.24.6.82`; external-dns meldde zes reconciles lang "All
      records are already up to date" terwijl alle routes
      `Accepted=True` waren. Conflictresolutie op resource: de Ingress
      wint. Gevolg voor de procedure: een cutover is het WEGHALEN van de
      Ingress, niet het bijzetten van de route
- [ ] 5.6 Upload boven de drempel én een request > 15s — bewijst dat de
      `timeouts` de Envoy-default vervangen. Nog te doen
- [ ] 5.7 Regressiesteekproef op drie niet-gemigreerde hosts;
      `kubectl get ingress -A | wc -l` blijft 236
- [ ] 5.8 MENS: eigenaar bevestigt functionele pariteit vóór er een
      DNS-record verhuist

## 6. Routes naar de generators (conventie) — afgerond 2026-08-17

- [x] 6.1 `React-base/charts/woo-website/templates/httproute.yaml` +
      `gatewayRoute`-values, opt-in met `gateway.frontend`. Twee nieuwe
      golden-testcases; 20 van 20 groen en géén bestaande golden
      gewijzigd, dus de andere tenants renderen byte-identiek
- [x] 6.2 `Nextcloud-base/charts/tenant-httproute` (HTTPRoute +
      ReferenceGrant), vierde source in `nextcloud-tenants`, opt-in met
      `gateway.nextcloud`. `sectionName` is verplicht en de chart faalt
      hard zonder — zie design.md besluit 7
- [x] 6.3 `tenant-canary-accept.yaml` zet beide vlaggen
- [x] 6.4 Tijdelijke constructie weg uit cluster-infra: Application
      `gateway-canary-routes` en `envoy-gateway/canary-routes/`
      verwijderd, `canary-accept` en `almere-accept` uit de
      `destinations` van het AppProject
- [x] 6.5 HTTP→HTTPS-redirect blijft in cluster-infra maar is
      hostname-loos: platformgedrag voor élke host in plaats van drie
      hardgecodeerde
- [x] 6.6 Docs: `cluster-infra/docs/gateway-api.md` herschreven,
      nieuwe `React-base/docs/GATEWAY-API.md` en
      `Nextcloud-base/docs/GATEWAY-API.md`, changelogs in drie repo's.
      `verify.sh` en pre-push groen in alle drie
- [ ] 6.7 MENS: `kubectl delete application -n argocd
      gateway-canary-routes` na de merge. Volgorde maakt niet uit — er
      loopt geen verkeer over de Gateway

## 7. Verify & archive

- [ ] 7.1 `./scripts/verify.sh` groen in cluster-infra; docs kloppen met
      wat er draait; CHANGELOG-entry bijgewerkt met het echte Envoy-IP
      en de meetresultaten uit fase 5
- [ ] 7.2 Archive this change

## Openstaand, niet in deze change

- **Wildcard-certificaat voor commonground.nu — dit blokkeert de hele
  Nextcloud-kant.** Elke host heeft nu een eigen HTTP-01-certificaat,
  dus elke tenant vraagt een eigen listener op de gedeelde Gateway met
  een eigen `certificateRef`. Werkt voor een canary, niet voor 84. Een
  DNS-01-wildcard voor `*.commonground.nu` en
  `*.accept.commonground.nu` — zoals al gedaan voor openwoo.app — lost
  dat op én haalt de HTTP-01-afhankelijkheid weg die nu elke cutover
  blokkeert. Zone staat bij Cloudflare, `letsencrypt-dns` bestaat.
  Hoort vóór de batch-migratie.
- Batch-migratie van de overige tenants, in door de operator gestuurde
  batches met een observatievenster per batch. Let op: een cutover is
  het weghalen van de Ingress, niet het bijzetten van een route
- Spike: kan de Keycloak-Operator Gateway API
- `--enable-gateway-api` op cert-manager, voor uitgifte via de Gateway
  zelf in plaats van via de achterblijvende Ingress
- `ReferenceGrant`/selector-verscherping van de Gateway — de eigenlijke
  isolatiewinst
- `ingress-nginx` uitfaseren
