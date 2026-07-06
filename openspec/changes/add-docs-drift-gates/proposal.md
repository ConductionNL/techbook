# Change: add-docs-drift-gates

## Why

Changes 1 and 2 make good documentation exist and be findable. Nothing yet
*keeps* it good: without enforcement, the baseline decays and the audit
becomes an annual archaeology exercise. This change turns drift into a
failing pipeline instead of a discovery after the fact — and doubles as
the ISO 27001 control that documented information is kept up to date,
evidenced by pipeline runs.

## What Changes

- Freshness gate: CI fails on pages whose `last_reviewed` is older than
  the configured maximum (default 365 days) or missing.
- External link gate: lychee over the built site; dead links fail the
  build. (Internal links already covered by `--strict` from change 2.)
- Scheduled rebuild: weekly cron on the handbook pipeline, so source-repo
  changes and freshness expiry surface without waiting for a handbook
  commit.
- Failure routing: a failed scheduled run creates/updates a single issue
  in the handbook repo (no silent red pipelines, no issue spam).

## Non-goals

- No style/terminology linting (Vale) in this change — valuable, but it
  needs a curated wordlist first; separate change once the gates run
  quietly for a month.
- No per-repo CI (gates run centrally in the handbook pipeline; source
  repos stay untouched).

## Rollout

Two-phase, deliberately: first month the freshness gate runs in
warn-only mode with findings in the job log, then it flips to blocking.
A gate that only warns forever is ignored — the flip date is part of
this change, not a later decision.

## Impact

- Affected specs: `docs-quality` (modified), `docs-portal` (modified)
- Affected repos: `Conduction/handbook` only
- Risk: low — worst case is a blocked docs deploy, never a blocked
  software release
