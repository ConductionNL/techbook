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

## 4. Bootstrap (mens doet elke cluster-actie)

Volgorde is niet vrij: elke stap `Synced Healthy` voor de volgende.

- [ ] 4.1 `kubectl apply -f argo/applications/gateway-api-crds.yaml`
- [ ] 4.2 `kubectl apply -f argo/applications/envoy-gateway.yaml`
- [ ] 4.3 `kubectl apply -f argo/applications/envoy-gateway-config.yaml`
- [ ] 4.4 Controleren dat de LoadBalancer een extern IP krijgt en de
      Gateway `Programmed=True` is; het IP vastleggen in de change
- [ ] 4.5 `kubectl apply -f argo/applications/gateway-canary-routes.yaml`

## 5. Canary valideren

- [ ] 5.1 Frontends: `curl -sI` op beide hosts, geldig wildcard-cert,
      200
- [ ] 5.2 Nextcloud via `--resolve` tegen het Envoy-IP: `status.php`
      200, `.well-known/webfinger` en `.well-known/caldav` 301,
      `config/config.php` 404
- [ ] 5.3 Poort 80 geeft 308 naar https, net als nginx vandaag
- [ ] 5.4 Upload boven de drempel én een request > 15s — bewijst dat de
      `timeouts` de Envoy-default van 15s vervangen
- [ ] 5.5 `strict-transport-security` en `access-control-*` vergelijken
      met dezelfde host via nginx; verschil = bevinding
- [ ] 5.6 Regressiesteekproef op drie niet-gemigreerde hosts vóór en na;
      `kubectl get ingress -A | wc -l` blijft 236
- [ ] 5.7 MENS: eigenaar bevestigt functionele pariteit vóór er een
      DNS-record verhuist. Voor de Nextcloud-canary verhuist er in deze
      change niets (HTTP-01-vernieuwing loopt over de nginx-Ingress)

## 6. Verify & archive

- [ ] 6.1 `./scripts/verify.sh` groen in cluster-infra; docs kloppen met
      wat er draait; CHANGELOG-entry bijgewerkt met het echte Envoy-IP
      en de meetresultaten uit fase 5
- [ ] 6.2 Archive this change

## Openstaand, niet in deze change

- Batch-migratie van de overige tenants, in door de operator gestuurde
  batches met een observatievenster per batch
- Spike: kan de Keycloak-Operator Gateway API
- `--enable-gateway-api` op cert-manager (voorwaarde voor een echte
  DNS-cutover van `*.commonground.nu`-hosts)
- `ReferenceGrant`/selector-verscherping van de Gateway — de eigenlijke
  isolatiewinst
- `ingress-nginx` uitfaseren
