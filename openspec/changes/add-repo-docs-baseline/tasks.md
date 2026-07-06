# Tasks: add-repo-docs-baseline

## 1. Contract definition

- [x] 1.1 Write the docs contract page (front-matter, Diátaxis, language
      rule) — lives in the future handbook repo's `docs/org/conventies.md`,
      for now at `docs/conventies.md` in this repo
- [x] 1.2 Write the repeatable audit checklist page (scope, checks,
      findings format) — `docs/audit-checklist.md`

## 2. Inventory

- [x] 2.1 List all Conduction repos on Codeberg with a `/docs` directory
      — done via local checkouts under ~/CONDUCTION instead of the
      Forgejo API (same result, no token needed): 17 repos with docs
- [x] 2.2 Decide participating set for phase 1 — decided (differs from
      proposal): react-base, Nextcloud-base, cluster-infra, KeyCloak,
      talos, cluster-config, monitoring, openwoo-app-config

## 3. Audit (zero-measurement)

- [x] 3.1 Script the mechanical checks: front-matter present/valid,
      duplicate-content candidates (fuzzy section matching), file inventory
      per repo — `scripts/check_docs_contract.py` (uv, plain output)
- [x] 3.2 Manual pass per repo: Diátaxis typing, accuracy vs current code,
      language rule
- [x] 3.3 Record findings per repo in `docs/audit-2026-07.md` (findings
      format from 1.2) — 63 mechanical findings, 5 duplication clusters

## 4. Remediation (one PR per repo)

- [ ] 4.1 Add front-matter to every page (reviewing content while adding —
      the review IS the `last_reviewed` date)
- [ ] 4.2 Split mixed-type pages; add cross-links
- [ ] 4.3 Replace duplicated content with links to canonical pages
- [ ] 4.4 Add CODEOWNERS rule for `/docs`
- [ ] 4.5 Ensure each `/docs` has an `index.md` (portal entry point later)

## 5. Verify

- [ ] 5.1 Re-run mechanical checks from 3.1: zero findings on participating
      repos
- [ ] 5.2 Archive this change
