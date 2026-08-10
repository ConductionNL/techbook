---
last_reviewed: 2026-08-10
owner: info@conduction.nl
---

# docs-touched (de diff-gate op docs-as-code)

`docs-contract` en `docs-claims` kijken naar de hele boom en nooit naar
wat je pusht. Daarmee werd §7 van de [conventies](conventies.md) —
"documentatie wijzigt in dezelfde PR als de code die zij beschrijft" —
door niets afgedwongen. `docs-touched` is de gate die dat wél doet.

Deze pagina is de referentie voor het configformaat, de vrijstelling en
het verificatierecept. De hookset als geheel staat in [hooks.md](hooks.md).

## Wat de gate doet

1. Bepaalt de diff van de push (`<from>...<to>`, met terugval op `..` als
   er geen merge-base is — dezelfde conventie als pre-commit zelf).
2. Loopt de commits in `<from>..<to>` langs, zonder merges, en bepaalt
   per commit welke paden docs-plichtig zijn.
3. Faalt wanneer er minstens één níet-vrijgestelde commit overblijft die
   docs-plichtige paden raakt terwijl er in de hele push geen
   docs-wijziging zit.

Docs-plicht wordt per commit opgebouwd, maar of eraan voldaan is wordt
tegen de héle push getoetst: eerst de code committen en daarna de docs
mag, want de norm is een eis per PR en niet per losse commit.

## Twee hendels die zwijgen in plaats van raden

- **Geen diff-context** (geen refs, dus ook bij `--all-files` en bij een
  root-commit, waar pre-commit `all_files=True` zet en géén refs
  meegeeft): de hook meldt "overgeslagen — geen diff-context" en geeft
  exit 0. Er wordt nooit een baseline zoals `origin/main` geraden; een
  gate die stiekem het verkeerde meet is erger dan geen gate.
- **Geen `.docs-touched.yaml`**: dezelfde zichtbare overslag. Dit maakt
  een uitrol over meerdere repos veilig — de hook kan overal aan staan
  terwijl elke repo op zijn eigen moment een config toevoegt.

Een `from_ref` die niet meer bestaat (force-push, opgeruimd object)
levert "kon diff niet bepalen" met exit 0, geen traceback.

## Configformaat

`.docs-touched.yaml` staat in de **repo-root**, niet in `args:` van
`.pre-commit-config.yaml`: `scripts/rollout_precommit_hook.sh` herschrijft
dat bestand in zijn geheel bij elke uitrol, dus padlijsten daarin
sneuvelen. Het pad is te overschrijven met `--config`.

    version: 1               # verplicht; onbekende waarde = harde fout
    mode: warn               # warn = rapporteren + exit 0, enforce = exit 1
    docs: ["docs/**", "README.md"]
    rules:
      - name: platform
        reason: "waarom dit pad docs-plichtig is — komt in de foutmelding"
        paths:   ["nextcloud-platform/**"]
        exclude: ["**/*.lock"]
        docs:    ["docs/platform/**"]   # optioneel, strenger dan globaal
    ignore: [".github/**"]
    escape:
      trailer: "Docs-not-needed"
      min_reason_len: 10
    git_timeout: 60          # seconden per git-aanroep
    report:
      max_files: 20          # hoeveel paden de foutmelding toont
      max_commits: 10

Alle drempels en patronen zitten in dit bestand; in het script staan
alleen defaults. Er is met opzet niets hardgecodeerd.

Patronen volgen **gitignore-semantiek** (via `pathspec`): `**` werkt zoals
in `.gitignore`, en een patroon zonder `/` (bijvoorbeeld `README.md`)
matcht op elk niveau. `docs/**` matcht alles ónder `docs/`, niet `docs`
zelf.

Precedentie bij matching: `ignore` > `rules[].exclude` > `rules[].paths`.
`ignore` zegt "deze wijziging vraagt geen docs" — het onderdrukt níet de
herkenning van docs-bestanden, anders zou `**/*.md` in `ignore` de gate
stilzwijgend onbruikbaar maken.

## Vrijstelling: per commit, niet per push

Een commit met de trailer is vrijgesteld en draagt geen eis bij:

    chore: witruimte in het values-bestand

    Docs-not-needed: alleen opmaak, geen gedragswijziging

Per push vrijstellen zou een gat zijn: één trailer op een triviale commit
zou een push van veertig bestanden vrijstellen. Een reden korter dan
`min_reason_len` (na `strip`) telt niet als vrijstelling.

## Uitrolvolgorde

Begin in `mode: warn`. De gate rapporteert dan volledig maar blokkeert
niets; na een rustige periode gaat hij naar `enforce`. Een gate die
eeuwig alleen waarschuwt wordt genegeerd, dus zet de omzetdatum vast op
het moment dat je `warn` kiest.

## Verificatierecept

Deze assertions draaien vanuit de repo-root, zonder cluster en zonder
netwerk:

```bash verify
test -f .docs-touched.yaml
grep -q '^version: 1' .docs-touched.yaml
grep -q 'Docs-not-needed' .docs-touched.yaml
grep -q 'id: docs-touched' .pre-commit-hooks.yaml
grep -q 'id: docs-touched' .pre-commit-config.yaml
test -x scripts/check_docs_touched.py
```

Het gedrag zelf controleer je met drie aanroepen; de eerste hoort over te
slaan, de andere twee horen tegengesteld te oordelen:

```bash
pre-commit run docs-touched --hook-stage pre-push --all-files --verbose
pre-commit run docs-touched --hook-stage pre-push \
  --from-ref origin/main --to-ref HEAD --verbose
scripts/check_docs_touched.py --from-ref origin/main --to-ref HEAD \
  --mode enforce
```

De foutmelding toont altijd de gebruikte refs en het aantal bestanden.
Ziet die diff er te breed uit, dan is een verouderde remote-tracking ref
de gebruikelijke oorzaak: `git fetch` en opnieuw.

## Testen

`tests/test_check_docs_touched.py` dekt de pure functies (matching,
precedentie, configvalidatie, trailer) en draait de gate op echte
tijdelijke git-repos — dit script bestaat om een diff te beoordelen,
dus alleen unit-tests zouden liegen. Draaien:

    uv run --with pytest --with pyyaml --with pathspec \
        python -m pytest tests/ -q
