# Tasks: add-agent-guardrails

## 1. Formaat en huisregels

- [x] 1.1 Cataloog-formaat vastgelegd (handbook org/agents.md:
      operatie | autonomie | idempotentie | verificatie; drie
      autonomie-niveaus) — (markdown-tabel: operatie |
      autonomie | idempotentie-bewijs | verificatie) + org-pagina
      "werken met agents" in het handboek
- [x] 1.2 Escalatieregel + standaardblok voor CLAUDE.md in dezelfde
      org-pagina — (niet-gecatalogiseerd =
      mens-vragen) in een gedeelde agent-instructieblok

## 2. Per component (~1 dag elk; volgorde op waarde)

Voor elke repo: cataloog schrijven → idempotentie per operatie
aantonen (verify/dry-run) → skills voor de top-taken → agent-instructies
naar docs-mcp wijzen.

- [x] 2.1 Nextcloud-base (2026-07-08): docs/agents.md (10 operaties),
      CLAUDE.md-blok, .mcp.json met conduction-docs, skill
      tenant-toevoegen (GET-check-first); verify + contract groen
- [ ] 2.2 react-base (frontend-blok-operaties, klein cataloog)
- [ ] 2.3 openwoo-app-config (provisioner is al idempotent — voorbeeldcase)
- [ ] 2.4 talos (egress-allowlist, workflows — hoge blast radius, strak)
- [ ] 2.5 monitoring (alert + runbook toevoegen)
- [ ] 2.6 KeyCloak (client-onboarding)
- [ ] 2.7 cluster-infra (component toevoegen)
- [ ] 2.8 cluster-config (scripts; klein)

## 3. Verify & archive

- [ ] 3.1 Scenario-test per component: herhaalde agent-run convergeert
      (geen diff bij tweede run); niet-gecatalogiseerde vraag escaleert
- [ ] 3.2 Archive this change
