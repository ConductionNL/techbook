# Spec Delta: docs-quality (add-docs-drift-gates)

## ADDED Requirements

### Requirement: Freshness gate

The portal pipeline SHALL fail when any page's `last_reviewed` date is
missing or older than the configured maximum age (default 365 days).
The gate SHALL apply to handbook-native pages and all aggregated pages.

#### Scenario: Page past maximum age

- WHEN the weekly build runs and a page's `last_reviewed` is 400 days old
- THEN the pipeline fails, listing the page path and its review date

#### Scenario: Reviewing a page resets the clock

- WHEN the owner reviews the page and updates `last_reviewed` to today
  (even with no content change)
- THEN the next build passes for that page

#### Scenario: Warn-only rollout phase

- WHEN the gate runs during the rollout month
- THEN findings appear in the job log but the pipeline succeeds; after
  the recorded flip date the same findings fail the pipeline

### Requirement: External link gate

The pipeline SHALL check all external links in the built site and fail
on dead links. Rate-limit responses (429) and bot-blocking responses
(403) SHALL NOT count as dead.

#### Scenario: Referenced external page removed

- WHEN a doc links to an external URL that now returns 404
- THEN the pipeline fails, identifying the page and the URL

### Requirement: Scheduled drift detection

The portal SHALL rebuild on a weekly schedule in addition to push
triggers, so drift in source repos and freshness expiry are detected
without a handbook commit.

#### Scenario: Source repo changes, handbook does not

- WHEN a participating repo's docs change on Tuesday and no handbook
  commit happens
- THEN the following Monday's scheduled run publishes the change and
  evaluates all gates against it

### Requirement: Failure routing

A failed scheduled run SHALL create an issue in the handbook repo, or
update the existing open one — never more than one open drift issue.

#### Scenario: Second consecutive failure

- WHEN the scheduled run fails while a drift issue is already open
- THEN the existing issue receives a comment with the new findings;
  no second issue is created

#### Scenario: Recovery

- WHEN a scheduled run succeeds while a drift issue is open
- THEN the issue is closed with a reference to the passing run
