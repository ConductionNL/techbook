# Change: add-repo-verify-gates

## Why

Northstar-pijler 1, tweede helft (verduidelijkt 2026-07-06): vóór elke
push moet niet alleen de documentatie kloppen (docs-contract gate,
bestaat) maar ook de **functionaliteit van de repo zelf** — unit tests,
dry-runs, render-checks. Nu bestaat dat versnipperd (openwoo heeft
`make test`, react-base heeft smoke-scripts, monitoring niets
aangesloten); niets dwingt het af.

## What Changes

- Elke deelnemende repo krijgt één standaard-entrypoint:
  `scripts/verify.sh` (of `make verify` waar een Makefile bestaat) —
  snel (richtlijn ≤ 2 min), **alleen dry-runs/render/tests, nooit
  cluster-mutaties**, exit-code als gate.
- Het entrypoint wordt als tweede pre-push hook gewired (pre-commit,
  `language: system`, lokaal per repo — naast de centrale
  docs-contract hook).
- Startinventaris per repo (uit te breiden in de verify-scripts):
  - openwoo-app-config: `make lint && make test` (bestaat al)
  - react-base: `validate-values.sh` + `smoke-checks.sh`
  - talos: `check-forgejo-runs-on.sh` + `kustomize build` beide overlays
  - monitoring: `promtool check rules` over `prometheus/rules/`
  - Nextcloud-base: tenant-values-validatie + `helm template` render
  - cluster-infra: kustomize/manifest-render + yaml-validatie
  - cluster-config: shellcheck + `check-shell-headers`
  - KeyCloak: yaml-validatie van realm-/CR-manifests
- Contract-pagina (`handbook org/conventies.md`) breidt uit: "Definition
  of Done = code + tests + docs; `verify` groen vóór push".

## Non-goals

- Geen centrale CI hiervoor (de gate is lokaal; centrale CI per repo is
  een latere, aparte afweging).
- Geen integratietests tegen live clusters — dry-run only.
- Verify-inhoud hoeft niet uniform te zijn; alleen het entrypoint en de
  semantiek (snel, read-only, exit-code) zijn de standaard.

## Impact

- Affected specs: `repo-quality` (new)
- Affected repos: alle 8 deelnemende repos + handbook (conventies-pagina)
- Risk: laag — een te trage of flaky verify wordt omzeild met
  `--no-verify` en verliest daarmee zijn waarde; daarom de harde
  snelheidsrichtlijn en dry-run-eis
