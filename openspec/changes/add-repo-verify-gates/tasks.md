# Tasks: add-repo-verify-gates

## 1. Standaard

- [ ] 1.1 Verify-conventie vastleggen in handbook `org/conventies.md`
      (entrypoint, ≤2 min, dry-run only, exit-code)
- [ ] 1.2 Pre-commit wiring-snippet bepalen (local hook,
      `language: system`, stage pre-push) + rollout-script uitbreiden

## 2. Per repo (één PR per repo; volgorde = makkelijk → zwaar)

- [ ] 2.1 openwoo-app-config — `make verify` als alias voor lint+test
- [ ] 2.2 cluster-config — shellcheck + check-shell-headers
- [ ] 2.3 monitoring — promtool check rules (promtool-beschikbaarheid
      op werkstations regelen of vendoren)
- [ ] 2.4 talos — label-guardrail + `kustomize build` beide overlays
- [ ] 2.5 react-base — validate-values + smoke-checks (afhankelijkheid:
      Nextcloud-base checkout — documenteren of automatisch clonen)
- [ ] 2.6 cluster-infra — manifest-render + yaml-validatie
- [ ] 2.7 KeyCloak — yaml/CR-validatie realm-manifests
- [ ] 2.8 Nextcloud-base — tenant-values-validatie + helm template render

## 3. Verify & archive

- [ ] 3.1 Bewijs per repo: kapotte wijziging wordt lokaal geblokkeerd
      (scenario uit de spec-delta), verify-tijd gemeten ≤ ~2 min
- [ ] 3.2 Archive this change
