# Spec Delta: repo-quality (add-repo-verify-gates)

## ADDED Requirements

### Requirement: Standard verify entrypoint

Every participating repo SHALL expose one verify entrypoint
(`scripts/verify.sh` or `make verify`) that runs the repo's fast
functional checks (unit tests, dry-runs, render checks) and exits
non-zero on any failure.

#### Scenario: New contributor runs verify

- WHEN someone runs the documented verify command in a fresh checkout
- THEN it completes without cluster access or credentials and reports
  pass/fail unambiguously

### Requirement: Verify is a pre-push gate

The verify entrypoint SHALL run automatically before every push (same
pre-commit mechanism as the docs-contract gate) and SHALL block the
push on failure.

#### Scenario: Broken change pushed

- WHEN a commit breaks a unit test or render and the author pushes
- THEN the push is blocked locally with the failing check named

### Requirement: Read-only and fast

Verify SHALL only read the working tree (no cluster mutations, no
writes outside temp dirs) and SHOULD complete within ~2 minutes, so
authors have no incentive to bypass it.

#### Scenario: Verify attempts a cluster call

- WHEN a verify script would need kubectl against a live cluster
- THEN that check is out of scope for verify and moves to a separate,
  explicitly invoked tool
