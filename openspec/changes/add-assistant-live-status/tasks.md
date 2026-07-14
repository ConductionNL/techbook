# Tasks: add-assistant-live-status

## 1. Besluiten (mens — trust-plane, per fase een go/no-go)

- [x] 1.1 MENS: GO fase 1 (Mark, 2026-07-14) — Argo-status via bestaande
      RBAC, nul nieuwe permissies
- [x] 1.2 MENS: GO fase 2 (Mark, 2026-07-14) op basis van design.md —
      route 1 (in-cluster Service-URL, env-tunable), catalogus van 8
      named queries; 9090/TCP t.z.t. expliciet in de egress-policy
      (genoteerd in de policy-kop)

## 2. Fase 1 — platform_status (Argo)

- [x] 2.1 Tool `platform_status` in assistant.py — 2026-07-14: argolib
      hergebruikt, drie vaste weergaven (samenvatting/degraded/alles),
      vrije input geweigerd, eigen MCP-server `platform`; 6 unit tests
      incl. backend-onbereikbaar (openwoo-app-config 2bc0322)
- [x] 2.2 Systeemprompt regel 6: live labelen (bron + tijdstip),
      backend weg = eerlijk + terugval op handboek — zelfde commit
- [x] 2.3 Audit: `status_calls`-veld per aanroep; record nu in `finally`
      (schreef eerder niets bij client-disconnect) — zelfde commit
- [x] 2.4 Image 0.3.2 live (2026-07-14, Argo Synced/Healthy). Bijvangst:
      `make push` verifieert nu de registry-tag (3× stille push-fout
      diezelfde dag; openwoo-app-config bb3727d)

## 3. Fase 2 — metrics_query (Prometheus, na 1.2)

- [x] 3.1 Query-catalogus vastgelegd — design.md (8 queries) + in code
      (METRIC_QUERIES) + deploy-README (2026-07-14)
- [x] 3.2 Route: in-cluster Service-URL (`PROMETHEUS_URL`, expliciet in
      deployment.yaml met 9090/TCP-egress-notitie; ook in de kop van
      networkpolicy-egress.yaml) — geen nieuw auth/ingress-oppervlak
- [x] 3.3 Tool `metrics_query` gebouwd (openwoo-app-config 3c7be29):
      alleen catalogus-namen, vrije PromQL geweigerd, eerlijk bij
      onbereikbare backend, status_calls-audit; 6 tests, suites groen
- [ ] 3.4 Image 0.4.0 bouwen/pushen (make release) + Argo-sync (mens),
      daarna live verify: metrics-vraag → "Live gemeten (bron:
      Prometheus …)" + status_call in audit

## 4. Verify & archive

- [x] 4.1 Scenario's aangetoond (2026-07-14): live vraag → antwoord
      "Live gemeten (bron: Argo CD, opgehaald …)" met status_call in het
      audit-record (weergave=degraded, apps=248); node-vraag → eerlijk
      "nog geen tool, fase 2"; vrije input en backend-uitval gedekt in
      unit tests (test_assistant.py)
- [ ] 4.2 Meedraaien in de proefdraaimaand van add-platform-assistant;
      kosten/nut evalueren
- [ ] 4.3 Archive
