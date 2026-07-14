# Tasks: add-component-skills

## 1. Besluit

- [x] 1.1 MENS: AKKOORD (Mark, 2026-07-14) — voorstel + fasering; fase 0
      direct gestart

## 2. Fase 0 — voorwaarden

- [ ] 2.1 `docs/agents.md` voor hub (3–5 operaties; o.a. clone_all,
      semantische-review, cataloog-audit)
- [ ] 2.2 `docs/agents.md` voor techbook (o.a. openspec-flow,
      contract/claims-checks, hook-rollout)
- [ ] 2.3 `docs/agents.md` voor handbook (o.a. org-pagina's bewerken;
      importlijst = trust root, expliciet mens-vereist)
- [ ] 2.4 monitoring: legacy `docs/AGENTS.md` archiveren (één
      agent-waarheid; case-collision weg)

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
