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
- [x] 3.3 Test private-repo clone with `DOCS_READ_TOKEN` against Forgejo —
      PROVEN in production (2026-07-06): KeyCloak turned out private;
      credential-store injection in the workflow authenticated the
      plugin's clone. (KeyCloak later removed from the public build for
      access reasons — the token path itself works.)
- [x] 3.4 Verify edit links on aggregated pages resolve to source repos —
      VERIFIED: plugin rewrites edit_uri per import (talos page →
      codeberg.org/Conduction/talos/_edit/main/docs/…)

## 4. Pipeline

- [x] 4.1 `.forgejo/workflows/docs.yml`: push to main + workflow_dispatch
      → uv sync --frozen → build --strict (met retry) → force-push naar
      de pages-branch
- [x] 4.2 Confirm the workflow runs on the existing self-hosted runners —
      as a container job on con-ci-oci (host class lacks node/curl);
      PyPI hosts added to that class's egress allowlist
- [x] 4.3 End-to-end proven: pushes to main build and publish the live
      site (first green run 2026-07-06 ~19:56)

## 5. Verify & archive

- [x] 5.1 Aggregation invariant PROVEN (2026-07-07 09:10): react-base
      docs changed at the source, workflow_dispatch rebuild, site
      updated with zero handbook commits
- [x] 5.2 Token scope review — reviewed 2026-07-07; **known deviation
      recorded**: DOCS_READ_TOKEN is a personal token (scope: repository
      read only). Machine account creation requires management; handed
      over (overdracht) 2026-07-07. Replace token + revoke personal one
      as soon as the account exists.
- [x] 5.3 Archive this change — archived as
      changes/archive/2026-07-07-add-handbook-portal; spec promoted to
      openspec/specs/docs-portal/
