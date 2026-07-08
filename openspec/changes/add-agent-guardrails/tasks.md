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
- [x] 2.2 react-base (2026-07-08): cataloog + assertie 'geen eigen
      tenant-bestanden' (bewaakt de Argo-ís-de-watcher-bewering)
- [x] 2.3 openwoo-app-config (2026-07-08): cataloog (provisioner als
      idempotentie-voorbeeldcase) + assertie genoemde make-targets bestaan
- [x] 2.4 talos (2026-07-08): strak cataloog (security-posture en
      secrets mens-vereist; crown-jewel en generieke labels verboden),
      CLAUDE.md, .mcp.json, plus de eerste doc-assertion (change 9,
      allowlist-hosts ↔ docs) in verify
- [x] 2.5 monitoring (2026-07-08): cataloog + assertie release: mon-label
      op elke regel (naast de bestaande alert↔runbook-dekking)
- [x] 2.6 KeyCloak (2026-07-08, op feature-branch): strak cataloog
      (autorisatie/secrets mensenwerk) + assertie genoemde manifest-paden
- [x] 2.7 cluster-infra (2026-07-08): cataloog + assertie Applications ↔
      index; verouderde CLAUDE.md-componentenlijst ververst; assertie ving
      cert-manager-config als ongedekt (gefixt)
- [x] 2.8 cluster-config (2026-07-08): cataloog (scripts schrijven
      autonoom, uitvoeren mensenwerk) + assertie scripts ↔ index

## 3. Verify & archive

- [ ] 3.1 Scenario-test per component: herhaalde agent-run convergeert
      (geen diff bij tweede run); niet-gecatalogiseerde vraag escaleert
- [ ] 3.2 Archive this change
