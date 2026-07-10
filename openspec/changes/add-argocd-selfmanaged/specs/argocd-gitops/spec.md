# Spec Delta: argocd-gitops (add-argocd-selfmanaged)

## ADDED Requirements

### Requirement: Argo CD is zelf declaratief beheerd

De installatie en configuratie van Argo CD SHALL volledig uit git komen
(cluster-infra): gepinde upstream-versie plus een expliciet delta.
Secrets SHALL nooit in git staan (ESO). Er SHALL geen Argo-configuratie
in het cluster bestaan die niet uit de repo herleidbaar is.

#### Scenario: Config-drift wordt zichtbaar

- WHEN iemand een Argo-ConfigMap (bijv. argocd-rbac-cm) handmatig
  wijzigt in het cluster
- THEN toont de Application `argocd` OutOfSync en is het verschil
  reviewbaar tegen de repo

#### Scenario: Reproduceerbare bootstrap

- WHEN het cluster opnieuw opgebouwd wordt
- THEN volstaat de gedocumenteerde bootstrap (één handmatige apply van
  de repo-manifests), waarna Argo zichzelf en de rest beheert

### Requirement: Adoptie zonder gedragswijziging

Het onder beheer brengen SHALL bewezen non-invasief zijn: vóór de
Application wordt aangemaakt is `kubectl diff` leeg, en de eerste sync
is een no-op. Prune en selfHeal SHALL uit staan tot na een
gedocumenteerde observatieperiode.

#### Scenario: Eerste sync

- WHEN de Application `argocd` voor het eerst synct
- THEN wijzigt er nul objecten in het cluster (no-op), aantoonbaar in
  de sync-result

### Requirement: Break-glass-route vastgelegd

Er SHALL een gedocumenteerde uitzondering bestaan voor het geval Argo
zichzelf onbruikbaar maakt: herstel door een mens met kubectl vanaf een
werkstation, met de eis dat de repo daarna weer leidend wordt gemaakt.

#### Scenario: Argo herstelt niet

- WHEN Argo CD zelf niet meer kan syncen
- THEN beschrijft de cluster-infra-doc de kubectl-herstelroute en de
  terugkeer naar repo-leidend beheer
