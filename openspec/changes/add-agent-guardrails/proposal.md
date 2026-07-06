# Change: add-agent-guardrails

## Why

Northstar-pijler 3: agents werken aan deze repos, en herhaalde
agent-runs moeten **convergeren, niet driften**. Vandaag hangt dat af
van sessiecontext en discipline; er is geen vastgelegde, per component
controleerbare set regels over wat een agent mag, hoe hij verifieert en
waarom een run idempotent is. Schatting (gebruiker): ~1 dag per
component.

## What Changes

Per deelnemende repo een **agent-bundel**, als code in de repo:

- `CLAUDE.md`/agent-instructies met het **operatie-cataloog**: welke
  handelingen een agent zelfstandig mag doen, welke alleen-met-mens
  (push, cluster-mutaties), en welke nooit.
- **Idempotentie-eis** per toegestane operatie: GET-check-first
  (openwoo's provisioner is het huispatroon — elke stap checkt eerst en
  slaat over wat al klopt), aantoonbaar via de verify-gate (change 6).
- **Skills** voor de terugkerende taken van die component (bijv.
  "tenant toevoegen", "egress-host toevoegen", "alert-runbook
  aanmaken") die het cataloog en de gates afdwingen in plaats van
  vrije improvisatie.
- **Grondwaarheid**: agent-instructies wijzen naar docs-mcp (change 5)
  als bron; de repo-docs zijn leidend boven trainingsdata.
- Handbook krijgt een org-pagina "werken met agents" (het cataloog-
  formaat, de escalatieregels, hoe je een nieuwe component onboardt).

## Non-goals

- Geen autonome agents op productie: de mens blijft de push- en
  apply-hand (bestaande hook-blokkade blijft de backstop).
- Geen framework-lock-in: het cataloog is markdown + skills, geen
  runtime.
- Niet alle 8 tegelijk: per component één dag, volgorde op waarde.

## Impact

- Affected specs: `agent-guardrails` (new)
- Affected repos: alle 8 + handbook (org-pagina); afhankelijk van
  changes 5 (docs-mcp) en 6 (verify-gates)
- Risk: middel — te strakke guardrails maken agents nutteloos, te losse
  maken ze gevaarlijk; daarom per component beginnen bij het cataloog
  en pas daarna skills
