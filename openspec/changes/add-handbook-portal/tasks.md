# Tasks: add-handbook-portal

## 1. Repo setup

- [ ] 1.1 Create `Conduction/handbook` and `Conduction/pages` on Codeberg
- [ ] 1.2 Resolve design open question 2 (Pages serving convention) and
      question 3 (site URL) — record answers in design.md
- [ ] 1.3 Create scoped tokens: `DOCS_READ_TOKEN` (org read-only),
      `PAGES_TOKEN` (write on pages repo); store as handbook repo secrets

## 2. Portal skeleton

- [ ] 2.1 `pyproject.toml` (uv; mkdocs-material, mkdocs-multirepo-plugin,
      pinned versions) + `uv sync`
- [ ] 2.2 `mkdocs.yml`: theme, nl/en search, `edit_uri`, nav for org pages
- [ ] 2.3 Org pages: `index.md`, `org/architectuur.md`, `org/onboarding.md`;
      move the contract page from change 1 to `org/conventies.md` (this
      becomes its canonical home; old location gets a link)

## 3. Aggregation

- [ ] 3.1 Add multirepo imports for the participating set (from change 1)
- [ ] 3.2 Local build test: `uv run mkdocs build --strict` with public
      repos
- [ ] 3.3 Test private-repo clone with `DOCS_READ_TOKEN` env substitution
      against Forgejo (design.md known constraint) — document outcome
- [ ] 3.4 Verify edit links on aggregated pages resolve to source repos;
      if the plugin doesn't rewrite them, record the limitation in
      design.md and in `org/conventies.md`

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
