# Spec Delta: agent-guardrails (add-component-skills)

## ADDED Requirements

### Requirement: Skills codify catalogued operations

Every participating repo SHALL provide a skill
(`.claude/skills/<operation>/SKILL.md`) for each core operation its
catalogue marks autonomous or proposal-first. A skill SHALL reference
the catalogue entry it implements, apply GET-check-first, state its
idempotent behaviour on re-run, include the verification step, and end
with the human hand-over (push/apply is never the skill's job).

#### Scenario: Skill follows its catalogue

- WHEN a skill is executed for an operation the catalogue marks
  proposal-first
- THEN the skill produces a reviewable proposal/diff and stops for a
  human decision, exactly as the catalogue prescribes

#### Scenario: Skill drift detected

- WHEN the monthly semantic review compares a skill against its
  catalogue entry and finds a contradiction
- THEN that is a finding routed to the component owner, like any other
  docs-vs-truth drift

### Requirement: Programme repos have catalogues too

The programme repos (hub, techbook, handbook) SHALL each contain an
operation catalogue like any participating component; "not in the
catalogue = human-required" applies there identically.

#### Scenario: Agent operates in a programme repo

- WHEN an agent is asked to change the handbook import list
- THEN the catalogue names that operation human-required (trust root)
  and the agent prepares a proposal only

### Requirement: One agent-truth per repo

A repo SHALL have exactly one agent operation catalogue; legacy or
duplicate agent-instruction files are removed or archived.

#### Scenario: Legacy file next to the catalogue

- WHEN a repo contains both `docs/agents.md` and a legacy agent file
- THEN the legacy file is archived and the catalogue is the single
  source
