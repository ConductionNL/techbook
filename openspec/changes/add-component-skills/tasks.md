# Tasks: add-component-skills

## 1. Besluit

- [x] 1.1 MENS: AKKOORD (Mark, 2026-07-14) — voorstel + fasering; fase 0
      direct gestart

## 2. Fase 0 — voorwaarden

- [x] 2.1 `docs/agents.md` voor hub — 2026-07-14 (hub 9f6aed8):
      clone_all/docs_mcp/semantische-review autonoom; cockpit-settings
      expliciet mens ("een agent die ze wijzigt keurt zijn eigen kooi")
- [x] 2.2 `docs/agents.md` voor techbook — 2026-07-14: proposen autonoom
      als vóórstel, goedkeuren mens; contract/claims-checks autonoom;
      hook-rollout en normatieve specs mens/change-gebonden
- [x] 2.3 `docs/agents.md` voor handbook — 2026-07-14 (handbook 6f1abf2):
      importlijst als trust root mens-vereist; org-pagina's autonoom
- [x] 2.4 monitoring: `docs/AGENTS.md` én legacy `.cursor/rules/`
      verwijderd, index-verwijzing rechtgezet (monitoring 71ea0a6).
      Bijvangst genoteerd: techbook/handbook missen scripts/verify.sh
      (northstar-pijler 1) en conventies.md is over twee repos
      gedupliceerd — beide pre-existent, apart op te pakken

## 3. Fase 1 — skills op de sterkste gates

- [ ] 3.1 Nextcloud-base: `tenant-wijzigen` en
      `tenant-verwijderen-voorbereiden` (patroon: tenant-toevoegen)
- [ ] 3.2 openwoo-app-config: `config-wijziging-flow`
      (export → sanitize → lint/test → commit)
- [ ] 3.3 monitoring: `alert-toevoegen-met-runbook` (runbook-gate dwingt
      de vorm af)
- [ ] 3.4 talos: `egress-host-toevoegen` (verplichte commentaarregel +
      doc-assertion)

## 4. Fase 2

- [ ] 4.1 cluster-infra: `component-values-wijzigen` +
      `component-toevoegen` (voorstel-eerst)
- [ ] 4.2 react-base: `vloot-render-check`
- [ ] 4.3 openspec-skillset: bron in techbook, uitrol naar alle
      openspec-repos
- [ ] 4.4 programma-skills hub/techbook/handbook (na hun catalogi)

## 5. Fase 3

- [ ] 5.1 KeyCloak: eerst docs-contract op peil (index.md, CODEOWNERS),
      dan `client-toevoegen-voorbereiden` (voorstel-eerst)
- [ ] 5.2 cluster-config: `script-toevoegen` + `rca-schrijven`
      (schrijf-skills; uitvoeren blijft mens)

## 6. Assistent-koppeling & afronding

- [ ] 6.1 Per fase-1-skill vastleggen welk read-only/voorstel-deel de
      webgui-assistent kan erven (input voor een latere
      assistent-change; uitvoerend deel blijft buiten de assistent)
- [ ] 6.2 Semantische-review-skill uitbreiden: skill-vs-cataloog-drift
      expliciet in de checklist
- [ ] 6.3 Archive
