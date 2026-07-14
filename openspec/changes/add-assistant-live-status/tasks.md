# Tasks: add-assistant-live-status

## 1. Besluiten (mens — trust-plane, per fase een go/no-go)

- [ ] 1.1 MENS: go/no-go fase 1 (Argo-status via bestaande RBAC, nul
      nieuwe permissies)
- [ ] 1.2 MENS: go/no-go fase 2 (Prometheus): toegangsroute + auth naar
      de monitoring-namespace (egress-historie meewegen: 2× DNS-breuk
      onder Gardener/Calico) én de named-query-catalogus vaststellen
      (voorzet: deployments-unavailable, node-saturatie, pod-restarts,
      PVC-vulling)

## 2. Fase 1 — platform_status (Argo)

- [ ] 2.1 Tool `platform_status` in assistant.py (hergebruik
      argolib/dashboard-poll; vaste weergaven: lijst + aggregatie);
      unit tests incl. backend-onbereikbaar
- [ ] 2.2 Systeemprompt + antwoordlabels: live data expliciet als live
      (bron + tijdstip), gescheiden van handboek-herkomst
- [ ] 2.3 Audit-record uitbreiden met tool/weergave per aanroep
- [ ] 2.4 Image + deploy (bestaand patroon; env-tunables conform regel:
      geen hardcoded limieten)

## 3. Fase 2 — metrics_query (Prometheus, na 1.2)

- [ ] 3.1 Query-catalogus vastleggen in docs (per query: naam, PromQL,
      wat hij beantwoordt, wat bewust niet)
- [ ] 3.2 Netwerkroute + auth naar Prometheus (monitoring); besluit
      documenteren in beide repos
- [ ] 3.3 Tool `metrics_query` (alleen catalogus-namen); unit tests
      incl. onbekende naam → weigering
- [ ] 3.4 Image + deploy

## 4. Verify & archive

- [ ] 4.1 Scenario's uit de spec-delta aantonen (live antwoord gelabeld;
      backend-uitval → eerlijk; vrije-query-poging → weigering;
      audit-record met tool-aanroep)
- [ ] 4.2 Meedraaien in de proefdraaimaand van add-platform-assistant;
      kosten/nut evalueren
- [ ] 4.3 Archive
