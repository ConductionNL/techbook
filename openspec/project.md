# Project Context

## Purpose

Conduction's technical documentation lives in the `/docs` directory of each
repository on Codeberg. A central portal (the "handbook") aggregates these
docs at build time. The core invariant: **content is never copied, only
aggregated**. Each repo's `/docs` is the single source of truth for that
project; the portal is a disposable build artifact.

## Problem being solved

Documentation drift: docs going stale relative to code, duplicated content
diverging across repos, and no periodic control on accuracy.

## Tech stack

- Git hosting: Codeberg (Forgejo), org `Conduction`
- CI: Forgejo Actions on self-hosted runners
- Portal: MkDocs Material + mkdocs-multirepo-plugin
- Python tooling via uv (never pip directly)
- Publishing: Codeberg Pages (`pages` repo in the org)

## Conventions

- Docs-as-code: docs change in the same PR as the code they describe
  (Definition of Done includes docs).
- Diátaxis: every page is exactly one of tutorial / how-to / reference /
  explanation.
- Front-matter contract on every page: `last_reviewed` (ISO date) + `owner`.
- Language: Dutch for organisation/client-facing pages, English for
  technical reference in open source repos; never mixed within one page.
- Boring and auditable over clever: standard tools, explicit config,
  everything explainable in an ISO 27001 audit.
- Files ≤ 200 lines.

## Change dependency order

1. `add-repo-docs-baseline` — per-repo audit and contract (no portal yet)
2. `add-handbook-portal` — aggregation portal (depends on 1)
3. `add-docs-drift-gates` — CI enforcement (depends on 2)
