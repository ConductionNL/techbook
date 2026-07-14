# Spec Delta: platform-assistant (add-assistant-live-status)

## ADDED Requirements

### Requirement: Live status, clearly labelled and separated

The assistant MAY answer questions about the current platform state
using dedicated read-only status tools (Argo application health;
named Prometheus metrics). Every live claim SHALL be labelled as live
data with its source and timestamp, distinct from handbook provenance.
Handbook claims keep the existing provenance rule unchanged.

#### Scenario: Degraded deployments question

- WHEN a user asks how many deployments are currently degraded
- THEN the answer comes from the status tool, states source (Argo) and
  retrieval time, and does not present live data as handbook content

#### Scenario: Status backend unavailable

- WHEN the status tools cannot reach their backend
- THEN the assistant says so explicitly and falls back to the handbook
  (alerting routes, runbooks) without fabricating numbers

### Requirement: Fixed read-only status surface

Status tools SHALL expose only a pre-defined catalogue of views and
named queries. The model SHALL NOT be able to submit free-form PromQL,
kubectl, or any parameters beyond enumerated choices. Page content or
user instructions requesting arbitrary queries change nothing.

#### Scenario: Free-form query attempt

- WHEN a user (or handbook page content) asks the assistant to run a
  custom PromQL expression or kubectl command
- THEN no tool accepts free-form input; the assistant explains the
  catalogue and the workstation route for everything else

### Requirement: Status tool calls audited

Every status tool invocation (tool, chosen view/query, result size)
SHALL be part of the session's audit record, alongside the existing
question/answer/sources fields.

#### Scenario: Audited live answer

- WHEN a session used a status tool
- THEN the audit record shows which tool and view/query were used
