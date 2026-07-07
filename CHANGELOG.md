# Changelog

## 2026-07-07 (middag) — change 6 geïmplementeerd: verify-gates in alle 8 repos

- Elke deelnemende repo heeft nu `scripts/verify.sh` (huisstijl-header,
  read-only, snel) als tweede pre-push hook naast docs-contract; alle
  hooks geherinstalleerd. Rollout-script uitgebreid (voegt verify-hook
  toe waar scripts/verify.sh bestaat).
- Conventie vastgelegd in handbook org/conventies.md §8.
- Bijvangst — de gates vonden meteen twee echte fouten:
  1. react-base validate-values.sh: jq-syntax in yq-aanroep (gefixt);
  2. Nextcloud-base tenant-vng-backend-green.yaml: resources/nextcloud
     op document-root i.p.v. onder tenant: — PLATFORMBESLUIT NODIG,
     de Nextcloud-base push blokkeert tot dan (bewust).
- Open: 3.1 (kapotte-wijziging-bewijs per repo) en promtool-installatie.

## 2026-07-07 (vervolg) — change 2 gearchiveerd

- `add-handbook-portal` gearchiveerd; `docs-portal`-spec gepromoveerd
  naar openspec/specs/ met een vastgelegde bekende afwijking:
  DOCS_READ_TOKEN is persoonlijk tot management een machine-account
  aanmaakt (overgedragen 2026-07-07); scope is al minimaal.

## 2026-07-07 — aggregatie-invariant bewezen; change 2 op token-review na af

- Dispatch-rebuild (09:10, geen enkele handbook-commit) publiceerde de
  aan de bron gewijzigde react-base-docs — kerninvariant van het portaal
  formeel aangetoond (taak 5.1). Taken 3.3, 4.1-4.3 ook afgevinkt
  (private-clone-pad in productie bewezen via KeyCloak; pipeline draait
  als container-job op con-ci-oci).
- Nog open in change 2: 5.2 (DOCS_READ_TOKEN vervangen door
  machine-account-token) en daarna 5.3 (archiveren).

## 2026-07-06 (nacht, vervolg) — changes 4-7 gespecct, README-verduidelijking

- Northstar verduidelijkt in openspec/project.md: pijler 1 omvat ook de
  functionaliteit van de repo zelf (unit tests / dry-runs als tweede
  pre-push gate) — nieuwe change 6 add-repo-verify-gates ertussen,
  agent-guardrails schuift naar 7.
- Vier changes gespecct (proposal + spec-delta + tasks):
  add-portal-access-split (4), add-docs-mcp (5), add-repo-verify-gates
  (6), add-agent-guardrails (7).
- README's van techbook en handbook openen nu met wat de repo wél/níet
  is en verwijzen naar elkaar (feedback: verschil was verwarrend).

## 2026-07-06 (nacht) — unit tests, hook-uitrol naar alle 8, northstar

- `tests/test_check_docs_contract.py`: 21 unit tests voor het
  contract-script (front-matter-parsing, repo-checks, duplicaat-detectie,
  exit-codes) — allemaal groen.
- `scripts/rollout_precommit_hook.sh` (shellcheck-schoon, idempotent):
  rolt de docs-contract pre-push gate uit; gedraaid over alle 8 repos
  (7 automatisch, talos handmatig gemerged in bestaande config;
  let op: KeyCloak-commit staat op de feature-branch).
- `openspec/project.md`: northstar vastgelegd (pre-push sync-gate met
  tests; handboek als agent-ingang via MCP; per component idempotente
  agents/skills/tools) + geplande changes 4-6 (portal-access-split,
  docs-mcp, agent-guardrails).

## 2026-07-06 (avond, later) — docs-contract als pre-push hook exporteerbaar

- `.pre-commit-hooks.yaml`: hook `docs-contract` (draait
  `scripts/check_docs_contract.py .` als pre-push gate) — zelfde
  export-patroon als talos' `forgejo-runs-on`. Consumer-repos pinnen
  techbook op een sha/tag; activatie per repo met
  `pre-commit install --hook-type pre-push`. Pilot: react-base.

## 2026-07-06 (avond) — change 2 gestart: handboek-portaal gescaffold

- Besluit (gebruiker): **één repo** — geen aparte pages-repo; de site
  wordt geserveerd van de `pages`-branch van `Conduction/handbook` op
  conduction.codeberg.page/handbook/ (Pages-conventie geverifieerd
  tegen docs.codeberg.org). Vastgelegd in proposal/design/tasks van
  `add-handbook-portal`.
- Handbook lokaal gescaffold (~/CONDUCTION/handbook): uv + MkDocs
  Material 9.7.6 + multirepo-plugin 0.8.3 (repos-modus), org-pagina's
  (conventies verhuisd als canonieke thuisbasis, architectuur,
  onboarding), Forgejo-workflow naar de pages-branch.
- Lokale strikte build groen: 83 pagina's, alle 8 imports; edit-links
  op geaggregeerde pagina's wijzen naar de bronrepo (spec-eis gehaald).
- Taken 1.2, 2.1–2.3, 3.1, 3.2, 3.4 afgevinkt; open: 1.1/1.3
  (repo + token aanmaken — gebruiker), 3.3 (private-clone-test, pas
  relevant bij een private repo), 4.x (pipeline live), 5.x.
- `docs/conventies.md` hier verwijst nu naar de canonieke versie in
  handbook.

## 2026-07-06 (vervolg) — remediatie alle 8 repos afgerond

Sectie 4 + taak 5.1 van `add-repo-docs-baseline` uitgevoerd. Hermeting:
**0 bevindingen** over de volledige deelnemende set.

- Per repo één commit "docs: baseline contract …" (talos, cluster-infra,
  KeyCloak, monitoring, openwoo-app-config, react-base, Nextcloud-base,
  cluster-config): front-matter, index.md, CODEOWNERS, en per repo de
  specifieke bevindingen (splitsingen, verplaatsingen naar root-/docs,
  drift-correcties — details in de commit messages van die repos).
- `docs/audit-2026-07.md`: remediatie-status + drie bewust geaccepteerde
  restpunten (Nextcloud-pagina's >200 regels, monitoring-huisstijl,
  duplicatie-clusters naar het handboek in change 2).
- `openspec/.../tasks.md`: 4.1–4.5 en 5.1 afgevinkt; 5.2 (archiveren
  van de change) staat nog open.
- Vervallen bevindingen gecorrigeerd in het auditdocument
  (monitoring-taal; tenant-docs bleken parallellen, geen duplicaten).

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
