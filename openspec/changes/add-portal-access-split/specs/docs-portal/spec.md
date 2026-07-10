# Spec Delta: docs-portal (add-portal-access-split)

## ADDED Requirements

### Requirement: Visibility classification per repo

Every imported repo SHALL carry an explicit `public` or `internal`
visibility in the handbook import list. There SHALL be no implicit
default.

#### Scenario: Import entry without visibility

- WHEN a PR adds an import entry without a visibility marker
- THEN the build fails, naming the entry

### Requirement: Public build excludes internal repos

The public site SHALL contain only repos marked `public` plus the
organisation pages. Docs from a private source repo SHALL never appear
in the public build.

#### Scenario: Private repo marked internal

- WHEN KeyCloak is marked `internal` and both variants build
- THEN its pages exist on the internal site and are absent from the
  public site (including the search index)

### Requirement: Internal site requires SSO

The internal site SHALL be reachable only after authentication via the
organisation's Keycloak (oauth2-proxy, fail-closed: unauthenticated
requests receive 403, health endpoint excepted).

#### Scenario: Unauthenticated request

- WHEN a request without a valid session hits any internal-site path
  except the health endpoint
- THEN the response is a redirect to login or 403, never page content

### Requirement: Role-scoped hosted MCP

The hosted MCP SHALL expose read tools to all authenticated users and
operation tools only to designated Keycloak roles; any change an
operation prepares SHALL materialise as a pull request in the source
repo — never a direct write or cluster mutation.

#### Scenario: Unprivileged user asks vs commands

- WHEN a user without the operations role calls a read tool and then an
  operation tool
- THEN the read succeeds and the operation tool is absent or refused
  for that identity

#### Scenario: Privileged operation

- WHEN a user with the operations role triggers a catalogued operation
- THEN the result is a reviewable PR in the source repo, and nothing
  changed until a human merges it
