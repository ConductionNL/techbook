# Change: add-assistant-live-status

## Why

De eerste echte gebruikssessie (2026-07-14) leverde direct vragen op als
"hoeveel deployments staan degraded?" en "welke CNI draaien we?". De
v1-assistent weigert die correct — hij is per spec handboek-only — maar
de vragen zijn legitiem, read-only beantwoordbaar, en gaan vaker komen.
Dit is een bewuste trust-plane-verschuiving (van "niets aan te roepen"
naar "alleen voorgedefinieerde reads") en vergt dus expliciete
menselijke goedkeuring vóór de bouw.

## What Changes

Twee fasen, elk achter een eigen menselijk besluit:

- **Fase 1 — `platform_status` (Argo, nul nieuwe permissies).** Nieuwe
  in-process tool die de Argo Applications leest via de RBAC die de
  webgui-pod al heeft (`rbac-argo.yaml`, cluster-scoped read-only voor
  de dashboard-poll): per applicatie naam, sync- en health-status, plus
  aggregaties ("N degraded"). Geen vrije input van het model — de tool
  kent alleen vaste weergaven.
- **Fase 2 — `metrics_query` (Prometheus, named queries).** Tool met een
  vastgelegde catalogus van benoemde PromQL-queries (o.a. deployments
  met unavailable replicas, node-saturatie/druk, pod-restarts, PVC-vulling)
  tegen de Prometheus van de monitoring-stack. Dekt de node-vragen die
  fase 1 niet kan. Het model kiest een query-náám, nooit vrije PromQL.
  Vergt netwerkroute + auth naar de monitoring-namespace (let op de
  egress-historie: 2× DNS-breuk onder Gardener/Calico — routekeuze is
  onderdeel van het besluit).
- **Overal:** live data wordt in het antwoord expliciet als live
  gelabeld (bron Argo/Prometheus + tijdstip), gescheiden van
  handboek-herkomst; elke tool-aanroep gaat mee in het audit-record;
  tool-uitvoer is data, geen instructie (bestaande injectie-regel).

## Non-goals

- Geen kube-API view-RBAC-tool (breedste optie; niet nodig zolang Argo +
  Prometheus de vragen dekken).
- Geen vrije PromQL of kubectl vanuit het model, ook niet "read-only".
- Geen schrijf- of execute-tools (v1-requirement blijft onverkort).
- Geen Grafana-embedding of dashboards in de chat.

## Impact

- Affected specs: platform-assistant (delta bij deze change)
- Affected repos: openwoo-app-config (assistant.py, tests, deploy);
  monitoring (Prometheus-toegangsroute + docs, fase 2)
- Risk: laag-middel — read-only, maar de assistent krijgt voor het
  eerst iets aan te roepen buiten het handboek; gemitigeerd door vaste
  query-catalogus, bestaande RBAC (fase 1), audit per tool-aanroep, en
  menselijke go/no-go per fase
