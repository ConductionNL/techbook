# Spec Delta: docs-claims (add-docs-claims)

## ADDED Requirements

### Requirement: Testable claims fail loudly

Every mechanically testable claim in participating docs SHALL be backed
by a check (doc-assertion or executable block) that fails the gate when
reality diverges from the documentation.

#### Scenario: Allowlist host undocumented

- WHEN a host is added to a squid allowlist without documenting it
- THEN the repo's verify gate fails, naming the host

### Requirement: Executable documentation blocks

Fenced code blocks marked `verify` SHALL be extracted and executed as
dry-runs by the shared runner: read-only, bounded by a timeout, exit
code gating the push and the weekly pipeline.

#### Scenario: How-to command rots

- WHEN a documented example command stops working (renamed script,
  removed flag)
- THEN the next push of that repo is blocked with the failing block and
  page named

#### Scenario: Marked block attempts mutation

- WHEN a `verify`-marked block would mutate cluster state or write
  outside temp dirs
- THEN review rejects it (same dry-run rule as repo-quality verify);
  the runner runs blocks with no cluster credentials by default

### Requirement: Coverage is visible

The runner SHALL report, per page, how many claims were tested. Zero
claims on a page is allowed but SHALL be visible in the report — never
an invisible gap that reads as coverage.

#### Scenario: Prose-only page

- WHEN a page contains no assertions or marked blocks
- THEN the report lists it with "0 claims" rather than omitting it

### Requirement: Semantic review for the rest

Prose that cannot be executed SHALL be reviewed on a recorded cadence
by an agent pass that compares docs against code and reports
contradictions through the existing drift-issue routing.

#### Scenario: Flow description diverges

- WHEN a documented flow no longer matches the implementing config
  (e.g. a generator reads a different directory than described)
- THEN the next semantic review pass files it as a finding with both
  sources cited
