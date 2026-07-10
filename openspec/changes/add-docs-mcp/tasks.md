# Tasks: add-docs-mcp

> NB 2026-07-10: repo hernoemd van `docs-mcp` naar `hub` (cockpit + MCP
> in één; gebruikersbesluit — nu herstructureren bij 9 repos, niet
> later bij 80). Servernaam blijft `conduction-docs`.

## 1. Skelet

- [x] 1.1 Repo opgezet (~/CONDUCTION/docs-mcp; mcp==1.28.1, pyyaml gepind) — (voorstel `Conduction/docs-mcp`): uv,
      MCP-SDK (python), pinned deps, unit tests vanaf dag één
- [x] 1.2 Importlijst-parser: leest handbook `mkdocs.yml`
      (multirepo.repos) → componentenlijst met url/branch/visibility

## 2. Content-laag

- [x] 2.1 Clone/refresh-beheer (fetch+reset, max-age-stamp, 0600 credential-file) —: shallow clones in een cache-dir,
      max-age (default 1u), DOCS_READ_TOKEN via credential store
      (zelfde patroon als de handbook-pipeline)
- [x] 2.2 Pagina-model: markdown + front-matter (owner, last_reviewed)
      + provenance

## 3. Tools

- [x] 3.1 `list_components` / `read_page` / `search_docs` (kale
      tekstsearch: titel > koppen > body, geen embeddings)
- [x] 3.2 Unit tests (12, netwerkvrij; incl. traversal- en token-lek-scenario's) — (fixture-repos, zoals bij
      check_docs_contract)

## 4. Distributie & verify

- [x] 4.1 Runnable + .mcp.json-snippet gedocumenteerd (docs-mcp/docs/gebruik.md; komt via de importlijst in het handboek) — + `.mcp.json`-snippet documenteren in het
      handboek (org/onboarding of eigen pagina)
- [ ] 4.2 OPEN: agent-sessie-test (registreren in .mcp.json, componentvraag beantwoorden); functionele livetest tools al groen — Live test: agent-sessie beantwoordt een componentvraag
      aantoonbaar uit de MCP-tools (provenance zichtbaar)
- [ ] 4.3 Scenario's uit de spec-delta aantonen; archive
