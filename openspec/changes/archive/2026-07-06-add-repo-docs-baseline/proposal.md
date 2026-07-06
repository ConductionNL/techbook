# Change: add-repo-docs-baseline

## Why

Before any portal exists, each participating repo's `/docs` must meet a
verifiable baseline. Aggregating stale or unstructured docs would publish
drift with a nice theme on top. This change defines the per-repo contract
and executes the initial audit — producing the zero-measurement that later
drift gates are checked against.

## What Changes

- Define the docs contract: front-matter (`last_reviewed`, `owner`),
  Diátaxis page typing, language rule (NL org-facing / EN technical).
- Audit every participating repo's `/docs` against the contract; record
  findings per repo (missing, stale, mixed-type, duplicated content).
- Remediate per repo via PR: add front-matter, split mixed pages,
  replace duplicated content with links to the canonical page.
- Add a CODEOWNERS entry for `/docs` in each participating repo.
- Publish the audit checklist itself as a doc (it is the repeatable
  control, not a one-off).

## Non-goals

- No portal, no CI gates yet (changes 2 and 3).
- No rewriting of content for style beyond what the contract requires.

## Impact

- Affected specs: `docs-quality` (new)
- Affected repos: every Conduction repo with a `/docs` directory
- Risk: low — pure documentation changes, reviewed via normal PR flow
