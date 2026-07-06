# techbook

Werkrepo voor het technische documentatie-handboek van Conduction. Het
handboek bundelt de `/docs` van componenten/repos in één doorzoekbaar
portaal — content wordt geaggregeerd, nooit gekopieerd; elke repo blijft
de bron van waarheid.

## Inhoud

- `openspec/` — het plan in drie changes: per-repo docs-baseline →
  handboek-portaal (MkDocs Material + multirepo) → drift-gates in CI.
- `docs/conventies.md` — het docs-contract (front-matter, Diátaxis,
  taalregel, locatie, geen duplicatie, CODEOWNERS).
- `docs/audit-checklist.md` — herhaalbare audit-procedure (ISO
  27001-bewijs voor actualiteit van documentatie).
- `docs/audit-2026-07.md` — nulmeting over de acht deelnemende repos.
- `scripts/check_docs_contract.py` — mechanische contract-check
  (uv-runnable, kale output, exit-code als gate).

## Status

Nulmeting afgerond (juli 2026): 63 mechanische bevindingen over
react-base, Nextcloud-base, cluster-infra, KeyCloak, talos,
cluster-config, monitoring en openwoo-app-config. Volgende stap:
remediatie-PR per repo (sectie 4 van
`openspec/changes/add-repo-docs-baseline/tasks.md`), daarna het portaal.

## Audit draaien

    uv run scripts/check_docs_contract.py <pad-repo-1> <pad-repo-2> ...

Exit-code 0 = geen bevindingen; 1 = bevindingen; 2 = aanroepfout.
