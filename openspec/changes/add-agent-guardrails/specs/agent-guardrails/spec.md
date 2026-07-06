# Spec Delta: agent-guardrails (add-agent-guardrails)

## ADDED Requirements

### Requirement: Operation catalogue per component

Every participating repo SHALL contain an agent operation catalogue
recording, per operation: autonomous / human-approval-required /
forbidden, plus the verification step that proves success.

#### Scenario: Agent asked to do an uncatalogued operation

- WHEN an agent is asked to perform an operation not in the catalogue
- THEN it treats the operation as human-approval-required and says so,
  rather than improvising

### Requirement: Idempotent execution

Every autonomous operation SHALL be idempotent: re-running it on an
already-correct state performs no writes and reports convergence
(GET-check-first pattern).

#### Scenario: Re-run on converged state

- WHEN an agent repeats an operation whose desired state already holds
- THEN no mutation occurs and the run reports "already converged"

### Requirement: Docs as ground truth

Agent instructions SHALL direct agents to the handbook (via docs-mcp)
as the authoritative source for component knowledge, above model
memory.

#### Scenario: Conflicting knowledge

- WHEN an agent's prior knowledge contradicts the current handbook page
- THEN the agent follows the handbook and may flag the discrepancy

### Requirement: Human hands on push and apply

Pushes to shared remotes and mutations of cluster state SHALL remain
human actions; agent tooling SHALL NOT bypass the existing blocks.

#### Scenario: Agent completes a change

- WHEN an agent finishes a repo change end-to-end
- THEN the final push command is handed to a human, never executed by
  the agent
