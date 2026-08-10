# Spec Delta: docs-quality (add-docs-touched-gate)

## ADDED Requirements

### Requirement: Docs-as-code diff gate

A pre-push gate SHALL fail a push when the pushed commits change paths
declared docs-requiring while no documentation changes in the same push.
The gate SHALL derive its scope from the push diff only, and SHALL NOT
infer a baseline when the refs are absent.

#### Scenario: Code changes without documentation

- WHEN a push contains a commit touching a docs-requiring path and the
  push contains no file matching the configured documentation patterns
- THEN the gate fails, naming the violated rule, its configured reason,
  the changed paths and the refs it compared

#### Scenario: Documentation in a later commit of the same push

- WHEN one commit changes a docs-requiring path and a later commit in the
  same push changes a documentation page
- THEN the gate passes, because the norm applies per PR, not per commit

#### Scenario: Path outside every rule

- WHEN a push only touches paths that no rule declares docs-requiring
- THEN the gate passes

#### Scenario: No diff context available

- WHEN the gate runs without ref arguments and without the pre-commit ref
  environment variables (as with `--all-files` or a root commit)
- THEN it reports that it is skipping for lack of diff context and exits
  successfully, without comparing against any assumed baseline

#### Scenario: Base ref no longer exists

- WHEN the recorded from-ref has been removed by a force-push or object
  pruning
- THEN the gate reports that it could not determine the diff and exits
  successfully, without a stack trace

### Requirement: Per-repo gate configuration

The gate SHALL read its rules from a configuration file in the repo root,
outside the pre-commit configuration file. Every threshold, pattern and
mode SHALL be configurable; the code SHALL contain defaults only. An
unrecognised configuration version SHALL fail hard rather than be
ignored. A missing configuration file SHALL be a visible skip.

#### Scenario: Repo without a configuration file

- WHEN a repo consumes the hook but has no configuration file yet
- THEN the gate reports the skip and exits successfully, so the hook can
  be rolled out across repos before each repo has written its rules

#### Scenario: Unknown configuration version

- WHEN the configuration declares a version the gate does not support
- THEN the gate exits with a configuration error, never silently

#### Scenario: Matching precedence

- WHEN a changed path matches both a rule's paths and its exclude list,
  or matches the repo-wide ignore list
- THEN ignore wins over exclude, and exclude wins over paths

#### Scenario: Warn mode

- WHEN the configured mode is warn and a rule is violated
- THEN the findings are printed in full and the push is not blocked

### Requirement: Per-commit exemption

Exemption SHALL be granted per commit through a configurable commit
message trailer carrying a reason. An exempted commit SHALL contribute no
documentation requirement; other commits in the same push SHALL still be
evaluated. A reason shorter than the configured minimum SHALL NOT exempt.

#### Scenario: One of two commits carries the trailer

- WHEN two commits each touch docs-requiring paths, one with a valid
  trailer and one without, and the push contains no documentation change
- THEN the gate still fails, reporting only the commit without the
  trailer

#### Scenario: Empty or token reason

- WHEN a commit carries the trailer with an empty or too-short reason
- THEN the commit is not exempted
