# Design / inventarisatie: add-argocd-selfmanaged

Bevindingen taak 1.x (2026-07-10, read-only tegen het cluster; werkkopieën
van export en diff op het werkstation, niet in git).

## Installatie

- Argo CD **v3.0.6**, upstream `manifests/install.yaml` (geen helm,
  geen HA-variant); alle images exact gelijk aan upstream.
- Cluster-scoped objecten (ClusterRoles/-Bindings) aanwezig conform
  upstream, aangemaakt 2025-06-18.

## Het delta t.o.v. upstream (volledig)

1. **Ingress `argocd-server-ingress`** — admin.commonground.nu (nginx,
   TLS via `argocd-server-tls`).
2. **`argocd-cm`**: `url`, `oidc.config` (Keycloak-SSO),
   `admin.enabled`, service-accounts `cluster-provisioner` en `syncbot`,
   en een `configManagementPlugins`-key (verouderde vorm sinds v2.5+ —
   kandidaat voor opruimen tijdens vastlegging).
   **SECURITY-FINDING (2026-07-10):** het OIDC-`clientSecret` staat
   **inline** in deze ConfigMap i.p.v. als
   `$oidc.keycloak.clientSecret`-verwijzing naar `argocd-secret`.
   Vastlegging MOET het secret eerst naar `argocd-secret` (ESO)
   verplaatsen — argocd-cm mag nooit as-is naar git. Overweeg rotatie
   van de client secret in Keycloak na de verhuizing (hij is nu leesbaar
   voor iedereen met CM-read in de namespace).
3. **`argocd-rbac-cm`**: `policy.csv`, `policy.default`, `scopes`.
4. **`argocd-ssh-known-hosts-cm`**: extra hosts (o.a. Codeberg).
5. **Credential-refresh-mechanisme** (het "mysterie", nu herleid):
   CronJob `argocd-credential-refresh` (elke 12u, image alpine/k8s)
   + ConfigMap met `refresh.sh` + eigen SA/Role/RoleBinding. Haalt via
   de **Gardener-API** verse 24u-kubeconfigs op voor de drie shoot-
   clusters (con-prod, conductionprod, test-accept) en schrijft die als
   `cluster-api.*`-secrets waarmee Argo die clusters bereikt.
   **Besluit 1.2: adopteren** — zonder dit verliest Argo binnen 24u de
   toegang tot alle beheerde clusters. Operationele bevinding: 3 van de
   laatste 6 runs faalden (17d/10d/3d geleden; nu groen) — bij
   vastlegging alerting overwegen (monitoring-repo).

## Secret-inventaris (taak 1.3 — niets hiervan in git)

| Secret | Rol | Beheer straks |
|---|---|---|
| `argocd-secret` | server-secret/admin/OIDC-client | ESO |
| `argocd-notifications-secret` | notificatie-creds | ESO |
| `argocd-server-tls` | TLS admin.commonground.nu | cert-manager |
| `gardener-sa-kubeconfig` | **root-credential** Gardener-API | ESO (nu handmatig geplaatst; geen ExternalSecret in de namespace) |
| `cluster-api.*` (3×) | runtime-artefact van de CronJob | NIET in git; door de CronJob beheerd |
| `nextcloud-repo-key`, `react-base-repo` | repo-creds | ESO |

## Consequentie voor scope

Argo beheert **drie shoot-clusters**, niet alleen zichzelf — het
zelfbeheer-manifest omvat dus ook het multi-cluster-toegangsmechanisme.
De kustomize-overlay in cluster-infra krijgt: ingress, de drie
CM-delta's, en het credential-refresh-geheel; secrets via ESO-manifests
die naar de secret-store verwijzen.
