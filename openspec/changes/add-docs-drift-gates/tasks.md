# Tasks: add-docs-drift-gates

## 1. Freshness gate

- [ ] 1.1 `scripts/check_freshness.py`: walk built/source docs tree,
      parse front-matter, fail on missing/expired `last_reviewed`
      (plain output, no colours/emoji — CI tooling; ≤200 lines; uv)
- [ ] 1.2 `--warn-only` flag + `--max-age-days` argument
- [ ] 1.3 Decide where the gate runs: on source `docs_dir` after the
      multirepo clone (preferred: page paths map to source repos) —
      verify the plugin's temp layout allows this
- [ ] 1.4 Wire into the workflow before the build step

## 2. Link gate

- [ ] 2.1 `lychee.toml`: accept 403/429, exclude localhost and Forgejo
      `_edit/` URLs, sane concurrency/timeouts
- [ ] 2.2 Wire lychee into the workflow after the build (runs on `site/`)
- [ ] 2.3 Confirm the lychee action/binary is available on the
      self-hosted runners; otherwise pin the binary in the container image

## 3. Schedule + failure routing

- [ ] 3.1 Add weekly cron trigger + `workflow_dispatch` to the workflow
- [ ] 3.2 Failure step (only on schedule): create-or-update a single
      `docs-drift` issue via Forgejo API; close it on the next green run
      — token needs issue write on handbook only; extend `PAGES_TOKEN`
      or add a separate scoped token (prefer separate)
- [ ] 3.3 Test all three paths: fail→issue created, fail→issue updated,
      pass→issue closed

## 4. Rollout

- [ ] 4.1 Enable freshness gate in `--warn-only`, record the flip date
      (one month out) in the workflow file as a comment and in the
      drift issue template
- [ ] 4.2 During warn month: burn down findings via source-repo PRs
- [ ] 4.3 Flip to blocking on the recorded date
- [ ] 4.4 Add a short how-to page to the handbook: "the docs pipeline is
      red — what now" (owner lookup, review procedure, gate config)

## 5. Verify & archive

- [ ] 5.1 Evidence check: confirm a pipeline run can serve as ISO 27001
      evidence for the document-currency control (run log shows checked
      pages + outcome)
- [ ] 5.2 Archive this change
