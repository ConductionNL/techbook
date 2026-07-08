# Change: add-docs-claims

## Why

De gates bewaken vorm (docs-contract) en werking (verify), maar geen
énkele controle toetst of wat de documentatie *beweert* nog waar is —
de react-base tenant-flow-drift werd door een mens gevonden, niet door
een gate. Northstar-uitspraak (2026-07-08): documentatie is het skelet
van de technische organisatie; wat erin staat moet **zelf toetsbaar**
zijn via tests en dry-runs, niet alleen leesbaar.

## What Changes

Drie lagen, van hard naar zacht:

1. **Doc-assertions** (per repo, in `scripts/verify.sh`): elke machinaal
   toetsbare bewering uit de docs wordt een falende check als hij niet
   meer klopt. Voorbeelden: elke host in een squid-allowlist is
   gedocumenteerd (talos), elk bestandspad dat docs noemen bestaat,
   elke alert heeft een runbook (monitoring — bestaat al, is het
   patroon).
2. **Uitvoerbare documentatie**: fenced codeblocks in docs kunnen
   gemarkeerd worden met info-string `verify` (```bash verify). Een
   gedeelde runner (geëxporteerd uit techbook als pre-commit hook
   `docs-claims`, net als `docs-contract`) extraheert die blokken en
   draait ze als dry-run: read-only, met timeout, exit-code als gate.
   Een how-to waarvan het voorbeeldcommando niet meer werkt, is dan
   rood in plaats van stilletjes gelogen.
3. **Agent-semantische review** (vangnet voor proza dat niet uitvoerbaar
   is): periodieke agent-pass per component — docs naast code leggen,
   tegenstrijdigheden melden via de bestaande drift-issue-routing.
   Bouwt op docs-mcp en de agent-catalogen (change 7).

Dekking wordt zichtbaar gemaakt: de runner rapporteert per pagina
hoeveel claims er getoetst zijn — nul claims is toegestaan (pure
uitleg-pagina's bestaan) maar nooit onzichtbaar.

## Non-goals

- Geen letter-voor-letter-garantie op vrij proza — laag 3 vángt, laag
  1/2 bewijzen; het verschil blijft expliciet.
- Geen verplichte claims op elke pagina; beginnen bij how-to's en
  referentie (daar staan de toetsbare beweringen).
- Marked blocks draaien nooit cluster-mutaties — dezelfde dry-run-eis
  als verify (repo-quality spec).

## Impact

- Affected specs: `docs-claims` (new), `repo-quality` (modified: verify
  omvat doc-assertions)
- Affected repos: techbook (runner + hook-export), alle deelnemende
  repos (assertions + gemarkeerde blokken, meegenomen in de
  cataloog-ronde van change 7), handbook (conventies §, weekly pipeline
  draait de claims mee)
- Risk: middel — te trage of flaky claims ondermijnen de gate-discipline;
  daarom dezelfde snelheids- en read-only-eisen als verify
