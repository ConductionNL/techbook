# Tasks: add-docs-claims

## 1. Gedeelde runner

- [x] 1.1 (2026-07-10) `scripts/check_docs_claims.py`: extraheert
      ```<taal> verify-blokken uit docs/, draait ze met timeout en
      zonder cluster-credentials, rapporteert claims per pagina
      (incl. "0 claims"); unit tests
- [x] 1.2 Geëxporteerd als hook `docs-claims`; techbook dogfoodt zijn
      eigen gates via een local pre-commit-config. Deelstap AF (2026-07-10):
      pin-bump + docs-claims-hook in alle 9 consumer-repos; keten
      gevalideerd; rollout-script schrijft de hook voortaan mee
- [x] 1.3 Conventie vastgelegd: handbook org/conventies.md §9

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
- [x] 2.4 Verify-blokken live in techbook (audit-commando), hub
      (import-check) en openwoo (make lint); meer blokken groeien
      organisch per docs-wijziging

## 3. Semantische laag

- [ ] 3.1 Agent-pass definiëren: cadans (voorstel: maandelijks per
      component), werkwijze (docs-mcp als bron, diff-gericht),
      uitvoer via de docs-drift issue-routing
- [ ] 3.2 Eerste pass over twee componenten als nulmeting

## 4. Verify & archive

- [ ] 4.1 Scenario's uit de spec-delta aantonen (rotte claim blokkeert;
      dekking zichtbaar; mutatie-blok geweigerd)
- [ ] 4.2 Archive this change
