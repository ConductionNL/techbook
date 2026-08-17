# Change: add-gateway-api-bootstrap

## Why

De ingress-laag van het platform draait op een dood project met een open
injectiegat.

`kubernetes/ingress-nginx` is op 2026-03-24 door upstream gearchiveerd:
read-only, geen CVE-patches meer. Het cluster draait v1.12.2 (gemeten
2026-08-17) met openstaande HIGH-CVE's, plus CVE-2026-42945 ("NGINX Rift")
die upstream sowieso niet meer gerepareerd wordt.

Ernstiger dan de versie is de configuratie. De controller draait met
`allow-snippet-annotations: true` en `annotations-risk-level: Critical`.
Daarmee kan élke namespace die een Ingress mag aanmaken willekeurige
nginx-configuratie injecteren — over ~50 gemeentetenants heen is dat een
doorbroken isolatiegrens, geen theoretisch risico. Het buiten deze change om
uitzetten van die vlag is containment; dit voorstel gaat over de structurele
opvolger.

Gateway API vervangt vrije-tekstconfiguratie door een getypeerde API. Die
overstap kan niet in één nacht: 236 Ingresses, 84 tenants, twee productlijnen.
Deze change zet de nieuwe laag ernaast en bewijst hem op drie routes.

## What Changes

- Gateway API + Envoy Gateway komen declaratief in **cluster-infra**, als vier
  Argo Applications naast de bestaande acht. Envoy Gateway omdat het cluster
  Calico draait: er is geen Gateway API-implementatie in de CNI.
- De CRD's worden **gevendord** uit de gepinde chart in plaats van door de
  chart geïnstalleerd, zodat er één eigenaar is en een chart-bump de CRD's niet
  stilzwijgend meeverandert. Zelfde lijn als de vendoring bij
  `add-argocd-selfmanaged`.
- Eén gedeelde `Gateway` met `allowedRoutes.namespaces.from: All` — bewust
  net zo permissief als de huidige Ingress-situatie. Verscherpen is de
  eigenlijke winst van de migratie maar hoort in een eigen change.
- Drie canary-`HTTPRoute`s **naast** de bestaande Ingress voor dezelfde host:
  twee WOO-frontends (die bewijzen het platform) en de Nextcloud van
  `canary-accept` (die bewijst de vertaling van timeouts, CORS en HSTS).
- `external-dns` leest ook `gateway-httproute`. Additief: zolang er geen
  HTTPRoute bestaat verandert er niets.
- Élke clustermutatie is mens-werk: de vier bootstrap-applies en de
  DNS-records.

## Non-goals

- De overige tenants migreren. Dat gaat in door de operator gestuurde batches
  met een observatievenster per batch, in een vervolgchange.
- `keycloak/keycloak-ingress`. De Keycloak-Operator genereert die Ingress zelf;
  of hij Gateway API kan is niet onderzocht — aparte spike.
- De 33 legacy Helm-Nextclouds in kale `<tenant>`-namespaces. Die staan op de
  nominatie om te verdwijnen.
- `ingress-nginx` uitfaseren. Pas als alle actieve tenants over zijn.
- De namespace-permissies verscherpen via `ReferenceGrant`/selector.
- De losstaande containment (controller-upgrade, `allow-snippet-annotations`
  uit). Deze change is daar niet van afhankelijk en andersom ook niet.

## Impact

- Affected specs: `gateway-routing` (new)
- Affected repos: `cluster-infra` (manifests, docs, verify); `Nextcloud-base`
  en `react-base` alleen als leesbron — hun ApplicationSets worden niet
  aangeraakt, de canary-routes staan tijdelijk in cluster-infra zodat de
  generators die 84 tenants voeden buiten schot blijven
- Cluster: een **tweede** OpenStack-loadbalancer met een eigen publiek IP,
  naast de `81.24.6.82` van nginx. Kostenpost en firewallregel.
- Risk: middel — een nieuw dataplane naast het bestaande. Gemitigeerd doordat
  geen enkele bestaande Ingress wordt aangeraakt, de canary's naast hun Ingress
  draaien, en de Nextcloud-canary in deze change géén DNS-wijziging krijgt
  (zijn certificaat wordt via HTTP-01 over de nginx-Ingress vernieuwd en dat
  zou bij een cutover breken).

## Premissen die tijdens het specen sneuvelden

Het oorspronkelijke voorstel rustte op een aantal aannames die niet tegen de
live staat overeind bleven. Ze staan hier omdat ze de scope veranderd hebben.

- De webfinger/nodeinfo/host-meta/CalDAV-set zou als `server-snippet` op ~34
  tenants staan en naar `URLRewrite`-filters vertaald moeten worden. Onjuist:
  voor GitOps-tenants zit die logica in de nginx-sidecar in de pod en blijft
  hij onveranderd achter de HTTPRoute staan. De 34 per-ingress snippets horen
  bij de legacy Helm-tenants en bevatten alleen twee headerregels. Het
  structurele punt van deze migratie is dus niet het wegwerken van rewrites,
  maar het wegnemen van de annotatieroute.
- Gateway API v1.2 pinnen. Verouderd: v1.5.1 hoort bij Envoy Gateway 1.8.3, en
  de CORS-filter is sinds v1.5 Standard — dus native, zonder Envoy-extensie.
- Canary's selecteren op "accept zonder CORS-annotatie". Zo'n tenant bestaat
  niet: `enable-cors` komt uit `common.yaml` en geldt fleet-breed. Die filter
  levert uitsluitend WOO-frontends op, en die kennen geen webfinger of CalDAV.
  Selectie gaat daarom op `tenant.wave: "0"` + `environment: accept`.
- `notify_push` valideren. Bestaat nergens in het platform.
