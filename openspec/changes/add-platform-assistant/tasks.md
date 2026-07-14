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
      webgui-namespace — GEPROBEERD EN TERUGGETROKKEN 2026-07-13: de
      policy (extern 443-only + DNS + kube-API + in-cluster HTTP; hostnaam-
      pinnen kan niet in vanilla Calico) brak DNS op prod ondanks correcte
      kube-system/53-regel — tweede bevestigde breuk onder Gardener/Calico.
      Bevindingen + debug-pod-experiment in de kop van
      `openwoo-app-config webgui/deploy/networkpolicy-egress.yaml`
      (file bestaat, staat uit de kustomization). Heropenen als los
      experiment, niet blokkerend voor de change
- [x] 3.3 Image + Argo-deploy volgens het bestaande webgui-patroon —
      LIVE 2026-07-13: image 0.3.0 (Dockerfile: git + hub gepind op sha
      met build-verificatie; claude-CLI gebundeld in de SDK-wheel),
      deployment-env/volumes/limits, secret `openwoo-assistant`
      (oauth-token, testfase-afwijking). Argo Synced/Healthy; /assistant
      werkt op platform.commonground.nu. Incident onderweg (apply van
      secret-template overschreef werkende secrets) verholpen en
      structureel gedefused — zie openwoo-app-config CHANGELOG 2026-07-13

## 4. Verify & archive

- [x] 4.1 Scenario's uit de spec-delta aangetoond — server-side via de
      model-benchmark (2026-07-13, 33 runs: gegrond mét bronnen,
      buiten-handboek-weigering, injectie-weigering op alle drie de
      modellen) én live op platform.commonground.nu door Mark (2026-07-14)
- [ ] 4.2 Maand proefdraaien met het team; kosten en kwaliteit reviewen.
      Modelkeuze (ASSISTANT_MODEL) volgt nadat het team de testset
      (webgui/benchmark.py, 11 vragen) zelf over de modellen heeft
      gedraaid — agent-run: default 9/9 (39s gem.), haiku 9/9 (21s gem.),
      sonnet 6/9 (intermitterende MCP-permissieweigering, apart uitzoeken)
- [ ] 4.3 Archive this change
