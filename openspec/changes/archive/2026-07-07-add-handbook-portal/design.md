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

**DECIDED 2026-07-06: single repo.** No separate `Conduction/pages` repo —
the built `site/` is force-pushed to a branch named `pages` **in the
handbook repo itself** (Codeberg Pages serves that at
`conduction.codeberg.page/handbook/`). Trade-off accepted: one repo to
manage beats the marginally cleaner source/artifact split; the artifact
branch has no history worth keeping (force-push, auditable via the
pipeline run log). Prefer the workflow's built-in Actions token for the
push to its own repo; fall back to a repo-scoped write token only if the
built-in token can't push.

### Edit links

`edit_uri` pointing at Forgejo's `_edit/main/docs/` path. The multirepo
plugin rewrites edit URIs per imported repo — verify this during
implementation; if it doesn't, accept edit links only on handbook-native
pages for v1 and note it as a known limitation.

## Open questions — RESOLVED 2026-07-06

1. Participating repo list for v1 (from change 1, task 2.2):
   react-base, Nextcloud-base, cluster-infra, KeyCloak, talos,
   cluster-config, monitoring, openwoo-app-config.
2. Codeberg Pages serves both ways (verified against
   docs.codeberg.org/codeberg-pages/): a repo named `pages` → org root
   URL; a branch named `pages` in any repo → `/reponame` subpath.
   Decision: **`pages` branch in the handbook repo** (single-repo setup).
3. Site URL: `https://conduction.codeberg.page/handbook/` (subpath) —
   set as `site_url`; canonical links follow.
