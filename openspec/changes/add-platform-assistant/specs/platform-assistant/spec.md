# Spec Delta: platform-assistant (add-platform-assistant)

## ADDED Requirements

### Requirement: Grounded answers with provenance

The assistant SHALL answer from the handbook content layer and SHALL
cite provenance (component, page, owner, last_reviewed) for every
substantive claim. When the handbook has no answer, it says so rather
than improvising.

#### Scenario: Question covered by the handbook

- WHEN a user asks how tenants are added
- THEN the answer reflects the current ADDING-TENANT pages and names
  its sources

#### Scenario: Question outside the handbook

- WHEN a user asks something no page covers
- THEN the assistant states that the handbook does not cover it and
  suggests the owner/escalation path, without fabricating

### Requirement: Read-only, authenticated, bounded

The v1 assistant SHALL expose no write or execute tools, SHALL sit
behind the existing SSO (fail-closed), and SHALL enforce per-user rate
and token budgets.

#### Scenario: Prompt-injected mutation attempt

- WHEN a user (or page content) instructs the assistant to change
  cluster state or files
- THEN no such tool exists to call; the assistant explains the
  workstation/catalogue route instead

### Requirement: Auditable sessions

Question, answer and cited sources SHALL be logged attributably
(SSO-identity), retention recorded; the API key SHALL live only as a
cluster secret.

#### Scenario: Audit review

- WHEN sessions are reviewed
- THEN each entry shows who asked what, what was answered and which
  pages were cited
