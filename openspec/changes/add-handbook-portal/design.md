# Design: add-handbook-portal

## Decisions

### MkDocs Material + mkdocs-multirepo-plugin

Chosen over Antora (would force AsciiDoc migration) and Backstage TechDocs
(a platform, not a docs tool — too much surface for this scale). MkDocs is
plain Markdown, Python/uv tooling, and the multirepo plugin does exactly
one thing: clone `docs/` from listed repos at build time.

Known constraint: the plugin shallow-clones over HTTPS. For private repos
the token goes into the import URL via env substitution — verify during
implementation that this works against Forgejo (plugin is developed
against GitHub; auth is plain basic-auth so it should, but test first).

### Repo layout

```
handbook/
├── mkdocs.yml            # nav + multirepo import list
├── pyproject.toml        # uv, mkdocs-material, multirepo plugin
├── docs/
│   ├── index.md
│   └── org/              # architecture, onboarding, conventions
└── .forgejo/workflows/docs.yml
```

Adding a repo to the portal = one PR touching only `mkdocs.yml`
(import entry + nav entry). This keeps participation explicit and
reviewable — no auto-discovery magic.

### Deploy mechanism

Force-push of the built `site/` to `Conduction/pages`. Deliberately dumb:
the pages repo has no history worth keeping because the source of truth
is elsewhere. Auditable via the pipeline run log, not via pages history.

### Edit links

`edit_uri` pointing at Forgejo's `_edit/main/docs/` path. The multirepo
plugin rewrites edit URIs per imported repo — verify this during
implementation; if it doesn't, accept edit links only on handbook-native
pages for v1 and note it as a known limitation.

## Open questions (resolve before apply)

1. Exact participating repo list for v1 (from change 1, task 2.2).
2. Does Codeberg Pages serve from `Conduction/pages` main branch or from
   a `pages` branch per repo? Confirm current Codeberg convention and
   set the push target accordingly.
3. Site URL: `conduction.codeberg.page` root or `/handbook` subpath —
   affects `site_url` and canonical links.
