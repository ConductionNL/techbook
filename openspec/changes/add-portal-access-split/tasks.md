# Tasks: add-portal-access-split

## 1. Config-splitsing

- [ ] 1.1 `mkdocs.yml` → basis + twee varianten via `INHERIT`
      (`mkdocs.public.yml`, `mkdocs.internal.yml`); visibility-marker
      per import-entry, build faalt zonder marker
- [ ] 1.2 KeyCloak terug in de internal-importlijst
- [ ] 1.3 Publieke site krijgt een pagina/banner die naar de interne
      variant verwijst

## 2. Interne site op het cluster

- [ ] 2.1 Dockerfile: nginx + `site-internal/` (statisch, non-root,
      readonly rootfs)
- [ ] 2.2 Keycloak-client `handbook` aanmaken (realm commonground;
      volg KeyCloak/docs/SSO-ONBOARDING.md)
- [ ] 2.3 Deploy-manifests naar het webgui-patroon: oauth2-proxy sidecar
      als enige listener, NetworkPolicy, Ingress + TLS; host bepalen
      (voorstel: docs.commonground.nu)
- [ ] 2.4 Argo Application (waar: cluster-infra of eigen map — besluiten)

## 3. Pipeline

- [ ] 3.1 Workflow bouwt beide varianten strict; public → pages-branch
      (als nu), internal → image build+push naar Codeberg registry
      (buildklasse con-ci-oci; registry-push-token als secret)
- [ ] 3.2 Argo pikt nieuwe image-tag op (digest-pin of tag+refresh —
      besluiten en vastleggen)

## 4. Gehost MCP-endpoint

- [ ] 4.1 docs-mcp: streamable-HTTP-transport naast stdio (zelfde tools,
      zelfde content-laag; geen extra schrijfpaden)
- [ ] 4.2 Deploy naar het cluster achter de oauth2-proxy → Keycloak-laag
      van dit change (eigen host of pad onder de interne site)
- [ ] 4.3 Verifieer de Claude remote-MCP OAuth-flow tegen
      oauth2-proxy/Keycloak; documenteer het aansluitrecept in
      handbook org/agents.md naast het lokale recept

## 5. Verify & archive

- [ ] 5.1 Scenario's uit de spec-delta aantonen (entry zonder marker
      faalt; KeyCloak-pagina's alleen intern; 403 zonder sessie)
- [ ] 5.2 DOCS_READ_TOKEN vervangen door machine-account-token
      (openstaand punt uit change 2, taak 5.2)
- [ ] 5.3 Archive this change
