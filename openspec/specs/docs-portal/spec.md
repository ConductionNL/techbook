# Spec: docs-portal

## Requirements

### Requirement: Aggregation without copying

The portal SHALL fetch each participating repo's `/docs` at build time
from the repo's main branch. Project documentation SHALL NOT be committed
to the handbook repo.

#### Scenario: Doc updated in a source repo

- WHEN a page in `zeef/docs` is changed on main and the portal is rebuilt
- THEN the published site reflects the change without any commit to the
  handbook repo

#### Scenario: Attempt to add project docs to handbook

- WHEN a PR adds project-specific documentation to the handbook repo
- THEN review rejects it, pointing to the canonical location in the
  project repo (only organisation-level pages live in handbook)

### Requirement: Strict build

The portal build SHALL run `mkdocs build --strict`, so broken internal
links and navigation errors fail the build rather than publish.

#### Scenario: Cross-repo link breaks after a page rename

- WHEN a page in one repo links to a renamed page in another repo
- THEN the build fails with the broken reference identified

### Requirement: Deploy to Codeberg Pages

A successful build on main SHALL publish the site to Codeberg Pages under
the Conduction org.

#### Scenario: Merge to main in handbook

- WHEN a PR is merged to main and the pipeline succeeds
- THEN the updated site is reachable at the Pages URL

### Requirement: Least-privilege credentials

Build credentials SHALL be scoped tokens: read-only for cloning source
repos, write limited to the pages repo. Personal tokens SHALL NOT be used.

#### Scenario: Token audit

- WHEN the tokens are reviewed
- THEN each token's scope matches exactly its single purpose and is
  attributable to the pipeline, not a person

### Requirement: Edit affordance points to the source repo

Every aggregated page SHALL expose an edit link that resolves to the page
in its source repo, not to the handbook repo.

#### Scenario: Reader spots an error on an aggregated page

- WHEN the reader clicks "edit this page" on a zeef doc in the portal
- THEN they land on the file in `Conduction/zeef` on Codeberg

## Known deviations

- **Least-privilege credentials** (2026-07-07): `DOCS_READ_TOKEN` is a
  personal token pending a machine account (management action,
  handed over via overdracht). Scope is already minimal (repository
  read only). Resolve by replacing the secret and revoking the
  personal token.
