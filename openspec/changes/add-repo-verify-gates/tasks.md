# Tasks: add-repo-verify-gates

## 1. Standaard

- [x] 1.1 Verify-conventie vastgelegd in handbook `org/conventies.md`
      (entrypoint, ≤2 min, dry-run only, exit-code)
- [x] 1.2 Pre-commit wiring-snippet bepaald (local hook,
      `language: system`, stage pre-push) + rollout-script uitbreiden

## 2. Per repo (één PR per repo; volgorde = makkelijk → zwaar)

- [x] 2.1 openwoo-app-config (0.8s: make lint+test, 116 tests) — `make verify` als alias voor lint+test
- [x] 2.2 cluster-config (bash -n + shellcheck, 4 scripts) — shellcheck + check-shell-headers
- [x] 2.3 monitoring (structuur + alert-runbook-dekking; promtool-
      fallback transparant — promtool nog installeren voor PromQL-check) — promtool check rules (promtool-beschikbaarheid
      op werkstations regelen of vendoren)
- [x] 2.4 talos (beide overlays gerenderd + kubeconform, guardrail,
      shellcheck; 1.2s) — label-guardrail + `kustomize build` beide overlays
- [x] 2.5 react-base (hele vloot + smoke-checks + shellcheck; 70s;
      bonus: jq-syntaxbug in validate-values.sh gefixt) — validate-values + smoke-checks (afhankelijkheid:
      Nextcloud-base checkout — documenteren of automatisch clonen)
- [x] 2.6 cluster-infra (yaml-parse + kubeconform; 1.7s) — manifest-render + yaml-validatie
- [x] 2.7 KeyCloak (yaml-parse + kubeconform CRD-catalogus; 1.4s;
      commit op feature-branch) — yaml/CR-validatie realm-manifests
- [x] 2.8 Nextcloud-base (validate-values + smoke-checks) — LET OP:
      gate vond direct een echte afwijking (tenant-vng-backend-green:
      resources/nextcloud op document-root i.p.v. onder tenant);
      platformbesluit nodig, push blokkeert tot dan — tenant-values-validatie + helm template render

## 3. Verify & archive

- [ ] 3.1 Bewijs per repo: kapotte wijziging wordt lokaal geblokkeerd
      (scenario uit de spec-delta), verify-tijd gemeten ≤ ~2 min
- [ ] 3.2 Archive this change
