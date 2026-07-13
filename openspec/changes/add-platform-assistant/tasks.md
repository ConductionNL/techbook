# Tasks: add-platform-assistant

## 1. Besluiten (mens/management)

- [ ] 1.1 ANTHROPIC_API_KEY (default): org-workspace, budget,
      eigenaarschap, ESO-secret. TESTFASE ontgrendeld 2026-07-10:
      persoonlijke sub-token van Mark als vastgelegde afwijking —
      de bouw is hiermee niet langer geblokkeerd
- [ ] 1.2 Retentie/privacy van de audit-log vaststellen

## 2. Dienst

- [x] 2.1 Assistent-endpoint in de webgui (Claude Agent SDK, Python):
      sessies server-side, docs-mcp-content-laag als library, alleen
      read-tools; unit tests — 2026-07-10: `webgui/assistant.py`
      (claude-agent-sdk 0.2.115, in-process MCP-server "handboek" met
      search_docs/read_page/list_components; ingebouwde tools ook
      expliciet disallowed), 18 tests
- [x] 2.2 Grenzen: rate limit per SSO-identiteit, token-budget per
      sessie, timeouts — 2026-07-10: 10 vragen/uur (schuivend venster),
      turn-cap 12, timeout 180s, vraaglengte-cap 2000; alles env-tunable.
      NB livetest: ±$1,07 nominale kosten en 40s per vraag — weegt mee
      bij besluit 1.1 (budget) en evt. ASSISTANT_MODEL
- [x] 2.3 Audit-log (wie/vraag/antwoord/bronnen), key via ESO —
      2026-07-10: JSONL via logger + optioneel ASSISTANT_AUDIT_LOG;
      record bevat ts/user/vraag/antwoord/bronnen/usage/kosten/duur.
      ESO-secret blijft onderdeel van 1.1/3.3 (testfase: sub-token
      uit de proces-omgeving, conform vastgelegde afwijking)

## 3. UI en deploy

- [x] 3.1 Chatvenster in de webgui (streamend antwoord, bronnen
      klikbaar naar de interne site) — 2026-07-10: /assistant +
      NDJSON-stream /api/assistant/ask; bronnen linken naar de
      Codeberg-bron (interne site volgt met change 4); card op home
- [ ] 3.2 Egress: api.anthropic.com + codeberg.org vanuit de
      webgui-namespace (NetworkPolicy/allowlist) — VOORBEREID 2026-07-13:
      `webgui/deploy/networkpolicy-egress.yaml` (apart terugdraaibaar
      object; hostnaam-pinnen kan niet in vanilla Calico → extern
      443-only + DNS + kube-API + in-cluster HTTP; risico-analyse en
      testchecklist in de file-kop). Apply + checklist = mens
- [ ] 3.3 Image + Argo-deploy volgens het bestaande webgui-patroon —
      VOORBEREID 2026-07-13: Dockerfile (git + hub gepind op sha met
      build-verificatie, claude-CLI zit gebundeld in de SDK-wheel),
      deployment-env/volumes/limits, secret-template `openwoo-assistant`,
      newTag 0.3.0. Bouwen/pushen (make image/push) en syncen = mens;
      image éérst pushen, dan mergen

## 4. Verify & archive

- [ ] 4.1 Scenario's uit de spec-delta aantonen (gegrond antwoord,
      buiten-handboek-weigering, injectie-poging, audit-entry)
- [ ] 4.2 Maand proefdraaien met het team; kosten en kwaliteit reviewen
- [ ] 4.3 Archive this change
