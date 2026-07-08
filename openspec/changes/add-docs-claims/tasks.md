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
- [x] 2.2 monitoring: alert ↔ runbook (bestond al) + release: mon-label-
      assertie toegevoegd (2026-07-08)
- [x] 2.3 alle 8 repos hebben een domeinspecifieke assertie (2026-07-08):
      talos allowlist↔docs, react-base geen-tenant-bestanden, openwoo
      make-targets, monitoring release-label, KeyCloak manifest-paden,
      cluster-infra Applications↔index, cluster-config scripts↔index,
      Nextcloud-base via validator/guardrails; generieke paden-assertie
      volgt met de runner (1.1)
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
