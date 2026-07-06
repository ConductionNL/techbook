# Changelog

## 2026-07-06 — nulmeting docs-baseline

Uitvoering van openspec change `add-repo-docs-baseline`, secties 1–3
(contract, inventaris, nulmeting). Remediatie (sectie 4) volgt per repo.

- `openspec/` als eigen commit vastgelegd zoals aangetroffen.
- `docs/conventies.md` — docs-contract: front-matter
  (`last_reviewed` + `owner`), Diátaxis-typering, taalregel, root-`/docs`
  met `index.md`, geen duplicatie, CODEOWNERS. Besluiten: norm is
  root-`/docs` (afwijkende locaties zijn een bevinding), owner-veld is
  `mark`.
- `docs/audit-checklist.md` — herhaalbare audit-procedure met
  bevindingenformaat en ernst-indeling.
- `scripts/check_docs_contract.py` — mechanische checks (181 regels,
  uv/PEP 723, alleen PyYAML). Draai over de acht deelnemende repos:
  63 bevindingen, exit-code 1.
- `docs/audit-2026-07.md` — nulmeting over de vastgestelde set
  (react-base, Nextcloud-base, cluster-infra, KeyCloak, talos,
  cluster-config, monitoring, openwoo-app-config): 0/63 pagina's met
  front-matter, nergens CODEOWNERS/index.md, 2 repos met docs buiten
  root-`/docs`, 5 duplicatie-clusters (handmatig). Signalering
  `age.agekey` in monitoring gecontroleerd: niet getrackt, niet in de
  historie, gedekt door .gitignore — vals alarm, geen actie.
- `docs/index.md` + `CODEOWNERS` — techbook voldoet aan het eigen
  contract (script geeft 0 bevindingen op techbook).
- README herschreven (was één regel) naar actuele scope; openspec
  `tasks.md` bijgewerkt: taken 1.1–3.3 afgevinkt.
