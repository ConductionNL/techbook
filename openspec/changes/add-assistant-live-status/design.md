# Design-input fase 2 (metrics_query) — besluit 1.2

Read-only geverifieerd op het cluster (2026-07-14): kube-prometheus-stack
in namespace `monitoring`; Prometheus achter Service
`mon-kube-prometheus-stack-prometheus:9090` (geen eigen ingress);
kube-state-metrics en node-exporter (11 nodes) actief.

## Voorgestelde named-query-catalogus

Het model kiest uitsluitend een naam; de PromQL ligt vast in code.

| Naam | PromQL | Beantwoordt |
|---|---|---|
| deployments-unavailable | `kube_deployment_status_replicas_unavailable > 0` | "Welke deployments draaien niet volledig?" |
| node-cpu-saturation | `1 - avg by(instance)(rate(node_cpu_seconds_total{mode="idle"}[5m]))` | "Hoe vol zitten de nodes qua CPU?" |
| node-mem-saturation | `1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)` | "Hoe vol qua geheugen?" |
| node-not-ready | `kube_node_status_condition{condition="Ready",status!="true"} == 1` | "Zijn alle nodes gezond?" |
| pod-restarts-1h | `sum by(namespace,pod)(increase(kube_pod_container_status_restarts_total[1h])) > 0` | "Wat crashloopt er?" |
| pvc-usage | `kubelet_volume_stats_used_bytes / kubelet_volume_stats_capacity_bytes > 0.8` | "Welke volumes lopen vol?" |
| pods-pending | `kube_pod_status_phase{phase="Pending"} == 1` | "Blijft er iets hangen op scheduling?" |
| pods-oomkilled | `kube_pod_container_status_last_terminated_reason{reason="OOMKilled"} == 1` | "Wordt er iets OOM-gekilld?" |

## Toegangsroutes (besluitpunt)

1. **In-cluster Service-URL** (`http://mon-kube-prometheus-stack-
   prometheus.monitoring.svc:9090/api/v1/query`) — aanrader: geen nieuw
   ingress/auth-oppervlak. Kanttekeningen: (a) de webgui-pod heeft nu
   géén egress-policy, dus dit werkt vandaag; komt de policy terug (na
   het egress-debug-runbook in openwoo-app-config), dan moet 9090/TCP
   naar monitoring er expliciet in; (b) check of een ingress-policy op
   de monitoring-namespace de webgui toelaat.
2. **Via Grafana-ingress** (datasource-proxy-API) — bestaande auth, maar
   extra hop, tokenbeheer, en bindt een interne tool aan een publiek
   endpoint.
3. **Eigen Prometheus-ingress** — afgeraden: nieuw publiek oppervlak
   zonder eigen auth.

Advies: route 1, met het egress-runbook als voorwaarde vóór herinvoering
van de policy en 9090 als expliciete regel daarin.
