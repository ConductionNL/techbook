# Tasks: add-docs-mcp

## 1. Skelet

- [ ] 1.1 Repo/map opzetten (voorstel `Conduction/docs-mcp`): uv,
      MCP-SDK (python), pinned deps, unit tests vanaf dag één
- [ ] 1.2 Importlijst-parser: leest handbook `mkdocs.yml`
      (multirepo.repos) → componentenlijst met url/branch/visibility

## 2. Content-laag

- [ ] 2.1 Clone/refresh-beheer: shallow clones in een cache-dir,
      max-age (default 1u), DOCS_READ_TOKEN via credential store
      (zelfde patroon als de handbook-pipeline)
- [ ] 2.2 Pagina-model: markdown + front-matter (owner, last_reviewed)
      + provenance

## 3. Tools

- [ ] 3.1 `list_components` / `read_page` / `search_docs` (kale
      tekstsearch: titel > koppen > body, geen embeddings)
- [ ] 3.2 Unit tests per tool (fixture-repos, zoals bij
      check_docs_contract)

## 4. Distributie & verify

- [ ] 4.1 uvx-runnable maken + `.mcp.json`-snippet documenteren in het
      handboek (org/onboarding of eigen pagina)
- [ ] 4.2 Live test: agent-sessie beantwoordt een componentvraag
      aantoonbaar uit de MCP-tools (provenance zichtbaar)
- [ ] 4.3 Scenario's uit de spec-delta aantonen; archive
