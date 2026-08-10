# Change: add-docs-touched-gate

## Why

The docs contract says documentation changes in the same PR as the code
it describes (`docs/conventies.md` §7), and the Definition of Done
repeats it. Nothing enforced it. Both exported hooks (`docs-contract`,
`docs-claims`) run with `always_run: true` over the whole tree; neither
script ever looks at a diff. A convention that only lives in prose is
the drift this programme exists to prevent.

## What Changes

- New exported pre-push hook `docs-touched`: fails a push when the
  commits being pushed touch docs-requiring paths without any
  documentation changing along with them.
- Per-repo configuration in `.docs-touched.yaml` in the repo root —
  path rules, mode, thresholds. Deliberately not in `args:` of
  `.pre-commit-config.yaml`, which `scripts/rollout_precommit_hook.sh`
  rewrites in full on every rollout.
- Per-commit exemption via the `Docs-not-needed: <reason>` trailer. Not
  per push: one trailer on a trivial commit must not exempt forty files.
- Two visible skip levers: no diff context (no refs, as with
  `--all-files` and root commits) and no config file. The gate never
  guesses a baseline such as `origin/main`.
- Techbook runs the gate on itself in `warn` mode (dogfooding).

## Non-goals

- No rollout to consuming repos in this change. Bumping the pin, adding
  a `.docs-touched.yaml` per repo and moving the hook source from
  Codeberg to GitHub is a separate step that can only happen after this
  lands in techbook main.
- No semantic judgement: the gate checks that documentation moved, never
  that it moved *correctly*. That stays human work, as with
  `docs-contract`.
- No commit-stage variant. The unit of the norm is the PR, and the
  pre-push stage is the last point where the whole set is visible.

## Rollout

Deliberately two-phase, same pattern as `add-docs-drift-gates`: every
repo starts in `mode: warn` (report, exit 0) and flips to `enforce` on a
date recorded when `warn` is chosen. A gate that only ever warns is
ignored, so the flip is part of the rollout decision and not a later one.

## Impact

- Affected specs: `docs-quality` (modified)
- Affected repos: `Conduction/techbook` only in this change
- Risk: low — worst case is a blocked push with a named rule and reason;
  the escape trailer and `warn` mode both keep work moving
