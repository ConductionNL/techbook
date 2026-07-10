# Change: add-platform-assistant

## Why

Het handboek is de agent-ingang (northstar 2), maar die ingang vereist
nu een werkstation met checkout en Claude Code. Collega's en
niet-technische gebruikers hebben die niet. `platform.commonground.nu`
(de gehoste control-plane uit openwoo-app-config, al achter
oauth2-proxy → Keycloak, en bewust generiek genoemd om te groeien)
is de natuurlijke plek voor **embedded assistent-sessies in de
browser**: vragen stellen over het platform, antwoorden gegrond in het
handboek, mét herkomst.

## What Changes

- Nieuw onderdeel in de webgui: een chatvenster dat server-side
  agent-sessies draait (Claude Agent SDK, Python) met als grondwaarheid
  de docs-mcp **content-laag** (importeerbaar als library — geen tweede
  waarheid, zelfde importlijst, zelfde max-age).
- **v1 is strikt lezend**: vragen beantwoorden met verplichte
  bronvermelding (component, pagina, owner, last_reviewed). Geen
  operaties, geen cluster-toegang, geen schrijf-tools.
- Toegang via de bestaande SSO-laag (fail-closed). **Model-auth
  (besluit 2026-07-10): default is een ANTHROPIC_API_KEY** uit een
  org-workspace (budget-capped, attribueerbaar aan de dienst) als
  cluster-secret (ESO), nooit client-side. Voor de testfase mag een
  persoonlijke CLAUDE_CODE_OAUTH_TOKEN (subscription) — vastgelegd als
  tijdelijke afwijking: persoonlijk, gedeelde rate-vensters, verbruik
  boekt op één persoon; vervangen vóór bredere openstelling.
- Kosten- en misbruikgrenzen: per-gebruiker rate limit, max tokens per
  sessie, en een audit-log van vraag/antwoord (herleidbaar, ISO-lijn).

## Non-goals

- Geen operatie-uitvoering vanuit de browser in v1 — de
  operatie-catalogen (change 7) definiëren wat ooit zou mogen, maar de
  push/apply-hand blijft een mens op een werkstation. Een v2 met
  voorbereide-diff-workflows is een aparte change ná ervaring met v1.
- Geen eigen kennisbank of prompt-curatie naast het handboek.
- Geen anonieme toegang.

## Impact

- Affected specs: `platform-assistant` (new)
- Affected repos: openwoo-app-config (webgui), talos/cluster-infra
  (egress: `api.anthropic.com` vanuit de webgui-namespace), handbook
  (org-pagina bijwerken)
- New secret: `ANTHROPIC_API_KEY` (ESO) — besluit + budget bij management
- Depends on: docs-mcp (klaar); onafhankelijk van change 4 (webgui heeft
  al een eigen SSO-laag)
- Risk: middel — LLM-antwoorden aan eindgebruikers; gemitigeerd door
  verplichte herkomst, alleen-lezen tools en de audit-log
