# Spec Delta: docs-mcp (add-docs-mcp)

## ADDED Requirements

### Requirement: Single source of truth

The MCP server SHALL serve content from the same import list as the
handbook and SHALL NOT maintain separately curated content.

#### Scenario: Repo added to the handbook

- WHEN a repo is added to the handbook import list
- THEN the MCP server exposes that repo's docs without a code change to
  the server itself

### Requirement: Freshness bound

Served content SHALL be no older than a configured maximum age
(default 1 hour): on first use after expiry the server refreshes its
clones before answering.

#### Scenario: Stale cache

- WHEN a page changed upstream 2 hours ago and the cache is older
- THEN a `read_page` call returns the new content, not the cached copy

### Requirement: Read-only tools with provenance

All tools SHALL be read-only. Every `read_page`/`search_docs` result
SHALL carry provenance: source repo, path, `owner` and `last_reviewed`
from the front-matter.

#### Scenario: Agent reads a page

- WHEN an agent calls `read_page("talos", "architecture.md")`
- THEN the response includes the markdown body plus repo, path, owner
  and last_reviewed — enough to cite and to judge staleness

### Requirement: Visibility respected

The server SHALL honour the visibility split from
`add-portal-access-split`: internal repos are only served when the
caller's configuration provides the read credential; without it they
are absent from list, search and read.

#### Scenario: No credential configured

- WHEN the server runs without DOCS_READ_TOKEN
- THEN KeyCloak (internal) appears nowhere in tool output, and public
  repos work normally
