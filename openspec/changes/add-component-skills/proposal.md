# Change: add-component-skills

## Why

De catalogi (spec `agent-guardrails`) definiëren per repo wát een agent
autonoom mag, maar niets codificeert hóe: elke sessie herontdekt de
flow. Nextcloud-base's `tenant-toevoegen`-skill bewijst het patroon —
een skill die het cataloog naspeelt (GET-check-first, voorstel-eerst,
verify-gates, push door een mens) maakt herhaalde runs convergent en
reviewbaar. Northstar-pijler "per component idempotente
agents/skills/tools" vraagt dit vlootbreed, en de assistent-northstar
(de webgui kan op termijn wat gescopede agents kunnen) vereist dat die
capabilities eerst als expliciete, geauditeerde skills bestaan voordat
ze server-side herbruikbaar zijn.

Inventarisatie 2026-07-14 (agent-run, alle 11 repos): skill-dekking is
scheef — alleen Nextcloud-base (5), talos (4, alleen openspec-*) en hub
(1) hebben skills; 8 van de 11 repos nul, terwijl hun catalogi wél
autonome operaties benoemen. En de drie programma-repos (hub, techbook,
handbook) missen zélf een operatiecataloog — per de escalatieregel is
elke operatie daar nu de facto mens-vereist.

## What Changes

1. Spec-delta op `agent-guardrails`: elke deelnemende repo heeft naast
   `docs/agents.md` minimaal één skill per autonome of
   voorstel-eerst-kernoperatie, in het referentieformat van
   `tenant-toevoegen` (cataloog-verwijzing, GET-check-first,
   idempotentie expliciet, verify-stap, mens-overdracht aan het eind).
2. Catalogi dichten waar ze ontbreken: hub, techbook en handbook krijgen
   elk een `docs/agents.md` (3–5 operaties, conform de
   onboarding-checklist die daar nota bene zelf voor bestaat).
3. De openspec-skillset (propose/explore/apply/archive) krijgt één bron
   (techbook) en wordt uitgerold naar alle openspec-repos (nu alleen
   Nextcloud-base en talos).
4. Opschoning: monitoring draagt naast `agents.md` nog een legacy
   `docs/AGENTS.md` (Cursor-tijdperk) — archiveren; één agent-waarheid
   per repo.
5. Waar mogelijk per skill een doc-assertion of verify-toets; de
   maandelijkse semantische-review toetst skill-tegen-cataloog-drift.

## Fasering

- **Fase 0 (voorwaarde):** catalogi hub/techbook/handbook +
  monitoring-opschoning. Zonder cataloog geen skill.
- **Fase 1 (sterkste machinale gates, bewezen patroon):** Nextcloud-base
  (`tenant-wijzigen`, `tenant-verwijderen-voorbereiden`),
  openwoo-app-config (`config-wijziging-flow`), monitoring
  (`alert-toevoegen-met-runbook` — de runbook-gate dwingt conformiteit
  af), talos (`egress-host-toevoegen` — doc-assertion dwingt docs mee).
- **Fase 2:** cluster-infra (`component-values-wijzigen`,
  `component-toevoegen` voorstel-eerst), react-base
  (`vloot-render-check`), programma-skills in hub/techbook/handbook,
  openspec-uitrol.
- **Fase 3:** KeyCloak (eerst docs-contract op peil: index.md,
  CODEOWNERS — identiteits-kritisch, bewust laatst) en cluster-config
  (alleen schrijf-skills; uitvoeren blijft cataloog-vast mensenwerk).

## Non-goals

- Geen nieuwe autonomie-niveaus en geen operaties buiten het cataloog.
- Geen skill die pusht, kubectl-mutaties doet of secrets aanraakt.
- Geen webgui-schrijfrechten: de assistent blijft strikt lezend; wat hij
  van skills erft is het read-only en voorstel-genererende deel, per
  aparte change (zoals add-assistant-live-status).

## Impact

- Affected specs: agent-guardrails (delta bij deze change)
- Affected repos: alle 11; schrijfwerk per fase in de betreffende repo
- Risk: laag — skills codificeren bestaand cataloog-gedrag; het echte
  risico (skill wijkt af van cataloog) wordt gedekt door de
  semantische-review en de verify-gates
