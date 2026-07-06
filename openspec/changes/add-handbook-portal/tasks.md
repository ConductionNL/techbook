# Tasks: add-handbook-portal

## 1. Repo setup

- [ ] 1.1 Create `Conduction/handbook` on Codeberg (single repo — the
      `pages` branch in this repo is the deploy target, no pages repo)
- [x] 1.2 Resolve design open question 2 (Pages serving convention) and
      question 3 (site URL) — resolved 2026-07-06, recorded in design.md:
      pages branch in handbook repo, site at
      conduction.codeberg.page/handbook/
- [ ] 1.3 Create scoped token `DOCS_READ_TOKEN` (org read-only) as
      handbook repo secret; pages push uses the built-in Actions token
      (fallback: repo-scoped write token)

## 2. Portal skeleton

- [x] 2.1 `pyproject.toml` (uv; mkdocs-material 9.7.6,
      mkdocs-multirepo-plugin 0.8.3, pinned) + `uv sync` — scaffolded
      locally at ~/CONDUCTION/handbook
- [x] 2.2 `mkdocs.yml`: theme, nl/en search, `edit_uri`, org pages
- [x] 2.3 Org pages: `index.md`, `org/architectuur.md`, `org/onboarding.md`;
      contract page moved to `org/conventies.md` (canonical home; techbook
      copy points there)

## 3. Aggregation

- [x] 3.1 Add multirepo imports for the participating set — `repos:` mode
      (nav-`!import` requires an mkdocs.yml in each source repo; repos
      mode does not — deliberate choice, recorded in handbook CHANGELOG)
- [x] 3.2 Local build test: `uv run mkdocs build --strict` green,
      83 pages, all 8 imports cloned from Codeberg (2026-07-06)
- [ ] 3.3 Test private-repo clone with `DOCS_READ_TOKEN` against Forgejo —
      OPEN: all v1 repos are public (anonymous clone worked); test the
      token path before the first private repo joins
- [x] 3.4 Verify edit links on aggregated pages resolve to source repos —
      VERIFIED: plugin rewrites edit_uri per import (talos page →
      codeberg.org/Conduction/talos/_edit/main/docs/…)

## 4. Pipeline

- [ ] 4.1 `.forgejo/workflows/docs.yml`: on push to main —
      uv sync → build --strict → deploy to pages
- [ ] 4.2 Confirm the workflow runs on the existing self-hosted runners
      (container image with git available; no privileged requirements)
- [ ] 4.3 End-to-end: merge a trivial handbook PR, verify the live site

## 5. Verify & archive

- [ ] 5.1 Change a doc in one source repo, trigger a rebuild manually
      (workflow_dispatch), confirm the site updates with zero handbook
      commits — this proves the aggregation invariant
- [ ] 5.2 Token scope review against the least-privilege requirement
- [ ] 5.3 Archive this change
