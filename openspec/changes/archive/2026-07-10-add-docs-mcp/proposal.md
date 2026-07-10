# Change: add-docs-mcp

## Why

Northstar-pijler 2: het handboek is DE ingang voor agents. Agents die
aan een component werken moeten de actuele, geaggregeerde documentatie
als grondwaarheid gebruiken — niet hun trainingsdata en niet een lokaal
verouderde checkout. MCP is daarvoor het standaardprotocol.

## What Changes

- Nieuwe MCP-server `docs-mcp` (Python, uv, minimale dependencies) met
  read-only tools:
  - `list_components()` — de deelnemende repos + hun index
  - `search_docs(query)` — zoeken over alle pagina's (titel, koppen,
    tekst; front-matter meegeleverd als metadata)
  - `read_page(component, path)` — één pagina als markdown, inclusief
    front-matter (owner, last_reviewed) en bronverwijzing
- Bron = de bronrepos zelf (shallow clone/pull per start of op interval),
  dezelfde importlijst als het handboek — geen tweede waarheid.
- Distributie: uvx-runnable vanuit een repo, geconfigureerd in de
  `.mcp.json`/agent-config van elke deelnemende repo (change 7 wijst
  agents erop).

## Non-goals

- Geen schrijf-tools (docs wijzigen blijft via PR's in de bronrepo).
- Geen embeddings/vector search in v1 — kale tekstsearch eerst; pas
  verzwaren als het aantoonbaar tekortschiet.
- Geen eigen hosting in v1 (stdio lokaal); een gehoste variant achter
  oauth2-proxy kan na change 4 (add-portal-access-split).

## Impact

- Affected specs: `docs-mcp` (new)
- New repo of map: voorstel `Conduction/docs-mcp` (klein, eigen tests)
- Hergebruik: importlijst uit handbook `mkdocs.yml` (parsen, niet
  dupliceren); DOCS_READ_TOKEN-patroon voor private repos
- Risk: laag — read-only; grootste risico is verouderde lokale cache,
  daarom een max-age op de content (zie spec)
