# Change: add-handbook-portal

## Why

With per-repo docs meeting the baseline (change 1), a central entry point
is needed: one searchable site covering all projects plus overarching
organisation docs. The portal must aggregate, never copy — otherwise it
becomes a second source of truth and reintroduces the drift problem it
exists to solve.

## What Changes

- New repo `Conduction/handbook` containing only:
  - overarching pages (architecture, onboarding, conventions — the
    contract page from change 1 moves here as its canonical home)
  - MkDocs Material configuration
  - multirepo aggregation config pulling `/docs` from participating repos
- Build pipeline (Forgejo Actions): `uv sync` → `mkdocs build --strict`
  → force-push `site/` to the `pages` branch of the handbook repo itself
  (DECIDED 2026-07-06: single repo, no separate pages repo; served at
  `conduction.codeberg.page/handbook/`)
- Read-only org token for cloning during build (private repos), scoped
  to repository read only

## Non-goals

- No drift gates yet (freshness, link checking, scheduled rebuilds are
  change 3) — this change only makes the portal exist and deploy on push.
- No theming beyond MkDocs Material defaults. Boring first.

## Impact

- Affected specs: `docs-portal` (new)
- New repos: `Conduction/handbook` (only)
- New secret: `DOCS_READ_TOKEN` (read-only org scope) in handbook repo
  secrets; the pages-branch push uses the workflow's built-in token
  (fallback: repo-scoped write token)
- Risk: low — portal is a build artifact; worst case is a broken site,
  never data loss
