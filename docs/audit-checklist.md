---
last_reviewed: 2026-07-06
owner: mark
---

# Audit-checklist documentatiekwaliteit

Herhaalbare procedure voor de periodieke audit van repo-documentatie
tegen het [docs-contract](conventies.md). Zo geschreven dat iemand anders
de audit identiek kan uitvoeren; de uitkomst dient als bewijs voor de
ISO 27001-beheersmaatregel dat gedocumenteerde informatie actueel wordt
gehouden.

## Scope bepalen

1. Stel de lijst deelnemende repos vast (bij twijfel: de importlijst in
   `handbook/mkdocs.yml` is leidend zodra het portaal bestaat).
2. Zorg voor een actuele lokale checkout van elke repo (main-branch,
   `git pull`).
3. Leg de lijst en de peildatum vast in het bevindingendocument.

## Mechanische checks (script)

Draai vanuit de techbook-repo:

    uv run scripts/check_docs_contract.py <pad-repo-1> <pad-repo-2> ...

Het script controleert per repo:

- `/docs` aanwezig in de repo-root
- `index.md` aanwezig in `/docs`
- CODEOWNERS aanwezig (root, `.github/`, `.forgejo/` of `docs/`)
- per pagina: front-matter met geldige `last_reviewed` (ISO-datum) en
  `owner`
- over alle repos heen: kandidaat-duplicaten (fuzzy match op koppen en
  openingsalinea — kandidatenlijst, menselijk oordeel vereist)

Exit-code 0 = geen bevindingen; 1 = bevindingen (staan in de output).
Bewaar de volledige output bij het bevindingendocument.

## Handmatige checks (per repo)

Het script kan taal, paginatype en juistheid niet beoordelen. Loop per
pagina na:

1. **Diátaxis-type**: is de pagina exact één type? Mengvorm = bevinding
   "splitsen" met voorstel welke twee pagina's het worden.
2. **Taalregel**: één taal per pagina; NL voor org-/klantgericht, EN voor
   technische referentie in open source.
3. **Accuraatheid**: klopt de inhoud nog met de huidige code/infra?
   Steekproef: volg één how-to daadwerkelijk; vergelijk referentie-pagina's
   met de bron (values-bestanden, CRD's, configs).
4. **Duplicaten beoordelen**: neem de kandidatenlijst van het script door,
   wijs per echt duplicaat de canonieke plek aan.

## Bevindingenformaat

Eén bevindingendocument per audit: `docs/audit-JJJJ-MM.md`, met per repo
een tabel:

| # | Pagina | Bevinding | Ernst | Actie |
|---|---|---|---|---|
| 1 | `docs/foo.md` | front-matter ontbreekt | laag | toevoegen bij remediatie-PR |

Ernst: **hoog** (inhoud aantoonbaar fout of misleidend), **middel**
(structuur belemmert vindbaarheid: verkeerde locatie, mengvorm, duplicaat),
**laag** (metadata/vorm: front-matter, CODEOWNERS, index).

Signaleringen buiten de docs-scope (bijv. vermoedelijke secrets in git)
komen in een aparte slotsectie "buiten scope, wel gesignaleerd" — niet
stilhouden, niet in deze audit oplossen.

## Afronden

1. Bevindingendocument vastleggen in techbook (later: handbook).
2. Remediatie: één PR per repo, bevindingen als checklist in de
   PR-beschrijving.
3. Na remediatie het script opnieuw draaien: nul mechanische bevindingen
   op de deelnemende set is het slotcriterium.
