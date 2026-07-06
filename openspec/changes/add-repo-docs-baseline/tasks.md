# Tasks: add-repo-docs-baseline

## 1. Contract definition

- [ ] 1.1 Write the docs contract page (front-matter, Diátaxis, language
      rule) — lives in the future handbook repo's `docs/org/conventies.md`,
      for now as a standalone Markdown file in this change
- [ ] 1.2 Write the repeatable audit checklist page (scope, checks,
      findings format)

## 2. Inventory

- [ ] 2.1 List all Conduction repos on Codeberg with a `/docs` directory
      (script: Forgejo API, read-only token)
- [ ] 2.2 Decide participating set for phase 1 (proposal: zeef,
      openanonymiser, wanderer; confirm against actual org)

## 3. Audit (zero-measurement)

- [ ] 3.1 Script the mechanical checks: front-matter present/valid,
      duplicate-content candidates (fuzzy section matching), file inventory
      per repo — plain output, no colours (one-shot tooling)
- [ ] 3.2 Manual pass per repo: Diátaxis typing, accuracy vs current code,
      language rule
- [ ] 3.3 Record findings per repo in `audit-2026-07.md` (findings format
      from 1.2)

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
