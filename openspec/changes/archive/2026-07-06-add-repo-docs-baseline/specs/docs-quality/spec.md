# Spec Delta: docs-quality (add-repo-docs-baseline)

## ADDED Requirements

### Requirement: Front-matter contract

Every Markdown page under `/docs` in a participating repo SHALL begin with
YAML front-matter containing `last_reviewed` (ISO 8601 date) and `owner`
(a resolvable person or team handle).

#### Scenario: Page with valid front-matter

- WHEN a page starts with `---`, contains `last_reviewed: 2026-07-06` and
  `owner: mark`, and closes with `---`
- THEN the page passes the contract check

#### Scenario: Page missing last_reviewed

- WHEN a page has front-matter without a `last_reviewed` field
- THEN the audit records a finding for that page

### Requirement: Diátaxis page typing

Every page SHALL be exactly one Diátaxis type (tutorial, how-to, reference,
explanation). Pages mixing types SHALL be split.

#### Scenario: Mixed page found during audit

- WHEN a page contains both step-by-step instructions and design rationale
- THEN the audit records a split finding, and remediation produces one
  how-to page and one explanation page linking to each other

### Requirement: No duplicated content across repos

Content SHALL exist in exactly one canonical location. Other locations
SHALL link to the canonical page instead of restating it.

#### Scenario: Same setup instructions in two repos

- WHEN the audit finds substantially identical sections in two repos
- THEN one location is designated canonical and the other is replaced by
  a link, recorded in the audit findings

### Requirement: Docs ownership

Each participating repo SHALL have a CODEOWNERS rule covering `/docs`,
so every docs change has an accountable reviewer.

#### Scenario: PR touching docs

- WHEN a PR modifies files under `/docs`
- THEN the CODEOWNERS-designated owner is requested for review

### Requirement: Repeatable audit checklist

The audit procedure itself SHALL be documented as a checklist page, so the
control can be re-executed (and evidenced for ISO 27001) without relying
on memory.

#### Scenario: Re-running the audit next year

- WHEN a new audit is planned
- THEN the checklist page describes scope, checks, and findings format
  such that a different person can execute it identically
