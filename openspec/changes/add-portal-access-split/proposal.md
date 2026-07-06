# Change: add-portal-access-split

## Why

The portal aggregates docs from public AND private repos, but Codeberg
Pages knows no authentication: KeyCloak's docs (internal endpoints,
client couplings) had to be pulled from the public site (2026-07-06).
Decision (user, same day): the hybrid model — a public portal for open
components and a complete internal portal behind SSO.

## What Changes

- Every entry in the handbook import list gets an explicit visibility:
  `public` or `internal` (no default — participation stays reviewable).
- Two builds from the same handbook repo:
  - **public**: only `public` repos + org pages → Codeberg Pages
    (`pages` branch, as today)
  - **internal**: everything → static site in an nginx image, deployed
    on the cluster behind **oauth2-proxy → Keycloak** (realm
    `commonground`) — the proven pattern from openwoo-app-config's
    webgui (fail-closed, sidecar as sole listener, NetworkPolicy)
- KeyCloak docs return, internal-only.
- Pipeline builds both variants; a page stating "je kijkt naar de
  publieke subset — interne versie: <url>" on the public site.

## Non-goals

- No per-page visibility (only per-repo) — keep the model auditable.
- No search across both variants; each site searches its own content.
- No change to the aggregation invariant (still build-time clone only).

## Impact

- Affected specs: `docs-portal` (modified)
- Affected repos: `handbook` (config + pipeline), `cluster-infra` or a
  new deploy repo for the internal site's Argo Application
- New secret: registry push token for the internal-site image
- Risk: low-medium — misclassification would expose internal docs;
  mitigated by no-default visibility + review on the import list
