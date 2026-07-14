---
last_reviewed: 2026-07-14
owner: info@conduction.nl
---

# Agent-cataloog (referentie)

Guardrails voor agents in deze repo, per het handboek-formaat
(org → Werken met agents). **Niet in dit cataloog = eerst vragen.**
Deze repo is normatief voor de hele vloot: de specs en het
docs-contract die hier staan, gelden overal — wijzigingen wegen
daarom zwaarder dan de bestanden doen vermoeden.

## Operaties

| Operatie | Autonomie | Idempotentie | Verificatie |
|---|---|---|---|
| Openspec-change proposen (`openspec/changes/<naam>/`: proposal, tasks, spec-delta's) | autonoom als **voorstel**; goedkeuren en starten van uitvoering doet een mens | tekstueel; bestaande change met dezelfde naam → eerst lezen, niet overschrijven | openspec-validatie waar beschikbaar; het voorstel benoemt expliciet wat het aan bestaande specs verandert |
| Afgeronde change archiveren (naar `openspec/changes/archive/`) | autonoom | al gearchiveerd → geen wijziging | alle taken in `tasks.md` afgevinkt; spec-delta's verwerkt in `openspec/specs/` |
| Contract-checks draaien (`scripts/check_docs_contract.py`, `scripts/check_docs_claims.py`) | autonoom | read-only (claims draaien als dry-run, zonder cluster-credentials) | exit 0 = geen bevindingen; bevindingen rapporteren, niet wegmasseren |
| Hook-uitrol (`scripts/rollout_precommit_hook.sh`) | mens-vereist | script slaat geconfigureerde repos over, maar commit per repo | raakt álle deelnemende repos tegelijk; agent bereidt hooguit de rev en het commando voor |
| Specs en normatieve teksten wijzigen (`openspec/specs/`, `docs/conventies.md`, hook-definities) | mens-vereist buiten een goedgekeurde openspec-change; binnen die change per de change zelf | tekstueel | de change is de audit-trail; losse edits aan normatieve tekst zijn drift per definitie |
| Push | mens-vereist | — | pre-push gates draaien bij de mens |

## Grondwaarheid en gedrag

- Handboek (MCP `conduction-docs`) boven modelkennis; voor de
  programma-regels zelf zijn `openspec/project.md` en de specs hier de
  diepste bron.
- GET-check-first: lees de bestaande change/spec vóór je een voorstel
  schrijft — een tweede voorstel voor hetzelfde probleem is ruis.
- Eigen tests (`tests/`) horen groen te zijn bij elke wijziging aan de
  check-scripts; de checks bewaken de vloot en verdienen dezelfde
  rigueur als de vloot zelf.
