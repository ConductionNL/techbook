# Tasks: add-docs-claims

## 1. Gedeelde runner

- [ ] 1.1 `scripts/check_docs_claims.py` in techbook: extraheert
      ```<taal> verify-blokken uit docs/, draait ze met timeout en
      zonder cluster-credentials, rapporteert claims per pagina
      (incl. "0 claims"); unit tests
- [ ] 1.2 Exporteren als pre-commit hook `docs-claims` (naast
      docs-contract); rollout-script uitbreiden
- [ ] 1.3 Conventie vastleggen in handbook `org/conventies.md`
      (markering, dry-run-eis, dekking zichtbaar)

## 2. Doc-assertions per repo (mee in de cataloog-ronde van change 7)

- [x] 2.1 talos: allowlist-hosts ↔ docs geïmplementeerd in verify.sh;
      eerste run ving pkg-containers.githubusercontent.com als
      ongedocumenteerd (gefixt). Paden-assertion volgt met de runner (1.1)
- [ ] 2.2 monitoring: alert ↔ runbook (bestaat al — geldt als patroon);
      genoemde paden bestaan
- [ ] 2.3 overige zes repos: minimaal de bestaande-paden-assertion +
      per repo één domeinspecifieke claim
- [ ] 2.4 Eerste verify-blokken in de meest gebruikte how-to's
      (tenant toevoegen, egress-host toevoegen, audit draaien)

## 3. Semantische laag

- [ ] 3.1 Agent-pass definiëren: cadans (voorstel: maandelijks per
      component), werkwijze (docs-mcp als bron, diff-gericht),
      uitvoer via de docs-drift issue-routing
- [ ] 3.2 Eerste pass over twee componenten als nulmeting

## 4. Verify & archive

- [ ] 4.1 Scenario's uit de spec-delta aantonen (rotte claim blokkeert;
      dekking zichtbaar; mutatie-blok geweigerd)
- [ ] 4.2 Archive this change
