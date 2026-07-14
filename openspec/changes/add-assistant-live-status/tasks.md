# Tasks: add-assistant-live-status

## 1. Besluiten (mens — trust-plane, per fase een go/no-go)

- [x] 1.1 MENS: GO fase 1 (Mark, 2026-07-14) — Argo-status via bestaande
      RBAC, nul nieuwe permissies
- [ ] 1.2 MENS: go/no-go fase 2 (Prometheus): toegangsroute + auth naar
      de monitoring-namespace (egress-historie meewegen: 2× DNS-breuk
      onder Gardener/Calico) én de named-query-catalogus vaststellen
      (voorzet: deployments-unavailable, node-saturatie, pod-restarts,
      PVC-vulling)

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

- [ ] 3.1 Query-catalogus vastleggen in docs (per query: naam, PromQL,
      wat hij beantwoordt, wat bewust niet)
- [ ] 3.2 Netwerkroute + auth naar Prometheus (monitoring); besluit
      documenteren in beide repos
- [ ] 3.3 Tool `metrics_query` (alleen catalogus-namen); unit tests
      incl. onbekende naam → weigering
- [ ] 3.4 Image + deploy

## 4. Verify & archive

- [x] 4.1 Scenario's aangetoond (2026-07-14): live vraag → antwoord
      "Live gemeten (bron: Argo CD, opgehaald …)" met status_call in het
      audit-record (weergave=degraded, apps=248); node-vraag → eerlijk
      "nog geen tool, fase 2"; vrije input en backend-uitval gedekt in
      unit tests (test_assistant.py)
- [ ] 4.2 Meedraaien in de proefdraaimaand van add-platform-assistant;
      kosten/nut evalueren
- [ ] 4.3 Archive
