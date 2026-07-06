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

## Northstar (recorded 2026-07-06)

1. **Working on a repo means staying in sync with its docs** — enforced
   mechanically before every push (the `docs-contract` pre-push gate,
   itself covered by unit tests) and substantively through docs-as-code
   review plus the freshness gate.
2. **The handbook is THE entry point for agents**, exposed via MCP:
   agents use the aggregated, current documentation as ground truth per
   component.
3. **Per component, agents/skills/tools are locked down for idempotent
   operation** — recorded guardrails per repo, so repeated agent runs
   converge instead of drift.

## Change dependency order

1. `add-repo-docs-baseline` — per-repo audit and contract (archived
   2026-07-06)
2. `add-handbook-portal` — aggregation portal (depends on 1)
3. `add-docs-drift-gates` — CI enforcement (depends on 2)

Planned next (northstar; propose in this order once 2–3 are archived):

4. `add-portal-access-split` — hybrid portal (decision 2026-07-06,
   option 3): public site for open components on Codeberg Pages,
   internal full site behind oauth2-proxy → Keycloak on the cluster
   (house pattern from openwoo-app-config's webgui). Until this lands,
   private-repo docs (KeyCloak) stay out of the public import list.
5. `add-docs-mcp` — expose the handbook via MCP as the agent entry point.
6. `add-agent-guardrails` — per-component agents, skills and tools with
   idempotency guarantees.
