# Tasks: add-platform-assistant

## 1. Besluiten (mens/management)

- [ ] 1.1 ANTHROPIC_API_KEY: budget, eigenaarschap, ESO-secret
- [ ] 1.2 Retentie/privacy van de audit-log vaststellen

## 2. Dienst

- [ ] 2.1 Assistent-endpoint in de webgui (Claude Agent SDK, Python):
      sessies server-side, docs-mcp-content-laag als library, alleen
      read-tools; unit tests
- [ ] 2.2 Grenzen: rate limit per SSO-identiteit, token-budget per
      sessie, timeouts
- [ ] 2.3 Audit-log (wie/vraag/antwoord/bronnen), key via ESO

## 3. UI en deploy

- [ ] 3.1 Chatvenster in de webgui (streamend antwoord, bronnen
      klikbaar naar de interne site)
- [ ] 3.2 Egress: api.anthropic.com + codeberg.org vanuit de
      webgui-namespace (NetworkPolicy/allowlist)
- [ ] 3.3 Image + Argo-deploy volgens het bestaande webgui-patroon

## 4. Verify & archive

- [ ] 4.1 Scenario's uit de spec-delta aantonen (gegrond antwoord,
      buiten-handboek-weigering, injectie-poging, audit-entry)
- [ ] 4.2 Maand proefdraaien met het team; kosten en kwaliteit reviewen
- [ ] 4.3 Archive this change
