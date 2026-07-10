# Change: add-argocd-selfmanaged

## Why

Argo CD is de trust-root van de hele GitOps-opzet, maar is zelf géén
GitOps: v3.0.6 draait als kale upstream-install (`kubectl apply`,
geen helm-release, geen Application die Argo beheert) en álle
Argo-configuratie — `argocd-cm`, `argocd-rbac-cm` (autorisatie!),
`argocd-notifications-cm`, de SSO-koppeling achter
admin.commonground.nu, plus een custom `argocd-credential-refresh-script`
ConfigMap zonder herkomst in enige repo — is onbeheerde clusterstate.
Gevolgen: cluster-rebuild is archeologie, RBAC-drift is onzichtbaar,
upgrades zijn handwerk zonder audit trail. ISO-technisch een finding;
gevonden via de assistent-livetest van change 10 (2026-07-10).

## What Changes

- Argo CD's eigen installatie en configuratie komen declaratief in
  **cluster-infra** (besluit 2026-07-10): kustomize-base op de gepinde
  upstream-versie + overlay met uitsluitend ons delta. Secrets nooit in
  git — via External Secrets (ESO), zoals de rest van het platform.
- Een Application `argocd` (project `cluster-infra`) gaat Argo zelf
  beheren. Volgorde is heilig: eerst bewijzen dat de eerste sync een
  **no-op** is (`kubectl diff` leeg), sync start **handmatig, zonder
  prune en zonder selfHeal**; pas na een bewezen no-op wordt selfHeal
  overwogen.
- Break-glass-route gedocumenteerd: als Argo zichzelf breekt, repareert
  een mens met kubectl vanaf een werkstation — die uitzondering op
  "alles via git" wordt expliciet vastgelegd, niet stilzwijgend.
- De herkomst van `argocd-credential-refresh-script` wordt herleid en
  ofwel geadopteerd (in git, gedocumenteerd) ofwel gepensioneerd.
- Docs: cluster-infra krijgt een pagina over het zelfbeheer + bootstrap
  ("eerste apply is handmatig, daarna beheert Argo zichzelf"), met een
  doc-assertion in verify (docs-claims).

## Non-goals

- Geen versie-upgrade van Argo CD in deze change (eerst vastleggen wat
  er draait; upgraden wordt daarna een gewone PR).
- Geen wijziging van bestaande Applications/Projects of hun sync-beleid.
- Geen migratie naar de helm-chart: we blijven bij upstream-manifests
  (dat is wat er draait; kleinste diff, geen nieuwe abstractie).

## Impact

- Affected specs: `argocd-gitops` (new)
- Affected repos: cluster-infra (manifests + docs + verify),
  handbook (org-architectuurpagina noemt het zelfbeheer)
- Cluster: uiteindelijk één nieuwe Application; de eerste sync is per
  definitie een no-op — tot die tijd verandert er niets aan het cluster
- Risk: middel — zelfbeheer kan bij een fout Argo zelf raken;
  gemitigeerd door no-op-bewijs vóór adoptie, handmatige sync zonder
  prune/selfHeal in de eerste fase, en de break-glass-route
