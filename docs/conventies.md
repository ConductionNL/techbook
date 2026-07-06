---
last_reviewed: 2026-07-06
owner: mark
---

# Documentatie-conventies (het docs-contract)

> **Canonieke thuisbasis:** deze pagina verhuist naar
> `handbook/docs/org/conventies.md` zodra het handboek-portaal bestaat
> (openspec change `add-handbook-portal`). Tot die tijd is dit de bron.

Dit contract geldt voor elke repo die meedoet aan het handboek. Het
portaal aggregeert de `/docs` van deelnemende repos; het contract zorgt
dat wat geaggregeerd wordt klopt, vindbaar is en actueel blijft.

## 1. Locatie

- Documentatie staat in `/docs` in de **root** van de repo.
- `/docs` bevat een `index.md` als ingang (het portaal gebruikt die als
  landingspagina van de component).
- Docs op andere plekken (submappen als `*-platform/docs/`, losse
  root-bestanden naast de README) zijn een bevinding: verplaatsen.

## 2. Front-matter

Elke Markdown-pagina onder `/docs` begint met YAML-front-matter met
precies deze twee verplichte velden:

    ---
    last_reviewed: 2026-07-06
    owner: mark
    ---

- `last_reviewed`: ISO 8601-datum (JJJJ-MM-DD) van de laatste inhoudelijke
  review. Een review zonder wijziging telt: de datum bijwerken ís de
  handeling die de houdbaarheid verlengt.
- `owner`: een bestaand, aanspreekbaar account op Codeberg (persoon of
  team). De owner is verantwoordelijk voor de juistheid van de pagina.

## 3. Paginatypes (Diátaxis)

Elke pagina is **exact één** van de vier types:

| Type | Beantwoordt | Voorbeeld |
|---|---|---|
| tutorial | "leer mij dit van nul" | eerste tenant opzetten, stap voor stap |
| how-to | "hoe doe ik taak X" | een tenant verwijderen |
| referentie | "wat zijn de feiten" | alle velden van het values-bestand |
| uitleg | "waarom zit het zo" | architectuurkeuzes, risico-afwegingen |

Een pagina die instructies én ontwerp-rationale mengt wordt gesplitst in
een how-to en een uitleg-pagina die naar elkaar linken.

## 4. Taal

- **Nederlands** voor organisatie- en klantgerichte pagina's.
- **Engels** voor technische referentie in open-source repos.
- **Nooit gemengd binnen één pagina.** Kies per pagina en houd vol;
  binnen één repo mogen beide talen voorkomen zolang elke pagina
  consequent is.

## 5. Geen duplicatie

Content bestaat op exact één canonieke plek. Andere pagina's linken
daarheen in plaats van het opnieuw te vertellen. Bij het aantreffen van
(bijna-)identieke secties in twee repos: één plek als canoniek aanwijzen,
de andere vervangen door een link.

## 6. Eigenaarschap

Elke deelnemende repo heeft een CODEOWNERS-regel die `/docs` dekt, zodat
elke docs-wijziging een verantwoordelijke reviewer heeft:

    docs/ @mark

## 7. Docs-as-code

Documentatie wijzigt in dezelfde PR als de code die zij beschrijft.
"Klaar" betekent: code, tests én docs bijgewerkt. Pagina's blijven
≤ 200 regels; wordt een pagina groter, dan is dat meestal een teken dat
er twee types (§3) in één bestand zitten.

## Naleving

De naleving wordt gecontroleerd met de herhaalbare audit
([audit-checklist](audit-checklist.md)) en — na openspec change
`add-docs-drift-gates` — automatisch in de handboek-pipeline
(freshness-gate op `last_reviewed`, linkcheck op de gebouwde site).
