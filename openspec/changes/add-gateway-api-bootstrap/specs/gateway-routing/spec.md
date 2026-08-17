# Spec Delta: gateway-routing (add-gateway-api-bootstrap)

## ADDED Requirements

### Requirement: De Gateway-laag is declaratief en gepind

Gateway API en zijn implementatie SHALL volledig uit git komen
(cluster-infra), met een expliciete versiepin en zonder `latest`. De
CRD's SHALL gevendord in de repo staan, niet uit een chart of een
remote branch komen, en hun herkomst (chart, digest, sha256, datum)
SHALL in de repo vastliggen. Er SHALL nooit een `kubectl apply` of
`helm install` tegen het cluster gaan buiten de gedocumenteerde
eenmalige bootstrap.

#### Scenario: Een CRD-bump is herleidbaar

- WHEN iemand de chartversie verhoogt
- THEN verandert het gevendorde CRD-bestand in dezelfde wijziging mee,
  is het opnieuw te genereren met het gedocumenteerde commando, en
  levert `diff` tegen de chart nul verschil

#### Scenario: Handmatige clusterwijziging wordt zichtbaar

- WHEN iemand een Gateway of GatewayClass in het cluster wijzigt buiten
  de repo om
- THEN toont de betreffende Application OutOfSync en is het verschil
  reviewbaar tegen de repo

### Requirement: CRD's worden nooit automatisch verwijderd

De Application die de CRD's beheert SHALL `prune: false` hebben. Het
verwijderen van een CRD SHALL een aparte, expliciete handeling van een
mens zijn.

#### Scenario: Een CRD verdwijnt uit de repo

- WHEN een CRD-definitie uit het gevendorde bestand wordt gehaald
- THEN verwijdert Argo het bijbehorende CRD niet uit het cluster, en
  blijven bestaande Gateways en HTTPRoutes bestaan

### Requirement: Migratie is coëxistentie, geen omzetting

Een tenant SHALL tijdens de migratie zowel zijn bestaande `Ingress` als
zijn nieuwe `HTTPRoute` hebben, met dezelfde backend-Service. Het
DNS-record SHALL pas verhuizen nadat de eigenaar functionele pariteit
heeft bevestigd. Terugdraaien SHALL geen dataplane-state hoeven
opruimen.

#### Scenario: Een canary faalt

- WHEN een HTTPRoute verkeerd blijkt te routeren
- THEN volstaat het verwijderen van die HTTPRoute (en het terugzetten
  van het DNS-record als dat al verhuisd was), en is er geen verlies
  omdat de Ingress altijd is blijven draaien

#### Scenario: Niet-gemigreerde tenants

- WHEN de Gateway-laag wordt uitgerold of gewijzigd
- THEN verandert er niets aan het verkeer van tenants die nog op
  ingress-nginx draaien, aantoonbaar met een steekproef vóór en na

### Requirement: Gedragspariteit wordt gemeten, niet afgeleid

De vertaling van ingress-annotaties naar HTTPRoute-filters SHALL
gebaseerd zijn op de response die de bestaande route daadwerkelijk
geeft, niet op de waarden in de values-bestanden. Een verschil tussen
beide SHALL als bevinding worden vastgelegd en niet stilzwijgend in de
migratie worden meegenomen of gerepareerd.

#### Scenario: Een annotatie blijkt een no-op

- WHEN een annotatie in de values een andere waarde heeft dan de header
  die de client ontvangt
- THEN krijgt de HTTPRoute de gemeten waarde, en wordt het verschil
  apart gemeld in plaats van in deze wijziging gecorrigeerd

### Requirement: Een migratie mag geen stille certificaatafhankelijkheid breken

Voordat een host van ingress-nginx naar de Gateway verhuist SHALL zijn
certificaat-vernieuwingspad zijn vastgesteld. Een host waarvan het
certificaat via HTTP-01 over de oude Ingress wordt vernieuwd SHALL niet
verhuizen voordat de Gateway die uitgifte kan overnemen.

#### Scenario: HTTP-01-host

- WHEN een host zijn certificaat via HTTP-01 over de nginx-Ingress
  vernieuwt en cert-manager's Gateway-ondersteuning nog uit staat
- THEN blijft het DNS-record naar ingress-nginx wijzen en wordt de
  HTTPRoute gevalideerd door de resolutie te forceren tegen het adres
  van de Gateway
