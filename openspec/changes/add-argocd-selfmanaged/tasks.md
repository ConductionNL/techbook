# Tasks: add-argocd-selfmanaged

## 1. Inventarisatie (read-only)

- [x] 1.1 Live Argo-objecten exporteren (cm/deploy/sts/svc/ingress/
      rbac — géén secrets) en diffen tegen de kale upstream
      v3.0.6-manifests: het eigen delta exact benoemen — 2026-07-10,
      zie design.md (delta = ingress + 3 CM's + credential-refresh)
- [x] 1.2 Herkomst en functie van `argocd-credential-refresh-script`
      herleiden (incl. wat hem mount/aanroept); besluit adopteren of
      pensioneren — 2026-07-10: CronJob die 24u-kubeconfigs voor de 3
      shoot-clusters ververst via Gardener; ADOPTEREN (zie design.md;
      3 van laatste 6 runs faalden — alerting-opvolgpunt)
- [x] 1.3 Secret-inventaris: welke secrets horen bij de install
      (SSO-client, repo-creds) en hoe lopen ze via ESO — 2026-07-10:
      tabel in design.md; gardener-sa-kubeconfig is nu handgeplaatst
      root-credential (geen ESO in de namespace)

## 2. Vastleggen in cluster-infra

- [x] 2.1 Kustomize-base op gepinde upstream-versie + overlay met
      uitsluitend het delta uit 1.1 — 2026-07-10: vendored (hermetisch)
      i.p.v. remote base; Application zonder prune/selfHeal/finalizer.
      AFWIJKING van de proposal: geen bruikbare ESO-backend aanwezig →
      gedocumenteerde bootstrap-secrets-lijst i.p.v. ESO (zie design.md)
- [x] 2.2 `kubectl diff` tegen het cluster tot die leeg is (no-op
      bewezen; dit is de gate voor 3.x) — 2026-07-10: restdiff = exact
      3 bekende, ongevaarlijke afwijkingen (OIDC-$-verwijzing, subject-
      namespace op 6 RoleBindings, herstelde labels op rbac-cm); de
      bootstrap-apply in fase 3 neemt ze weg, daarna diff leeg
- [x] 2.3 Docs: zelfbeheer + bootstrap + break-glass in
      cluster-infra/docs, doc-assertion in verify — 2026-07-10:
      docs/argocd.md (incl. upgrade-procedure en bootstrap-secrets-
      tabel), index/agents bijgewerkt, verify rendert+kubeconformt
      argocd/, docs-claims-blok getoetst

## 3. Adoptie (mens doet elke cluster-actie)

- [x] 3.1 Application `argocd` aanmaken (sync handmatig, geen prune,
      geen selfHeal); eerste sync aantoonbaar no-op — 2026-07-10:
      adoptie via scripts/argocd-adopt.sh (stap 1-3, mens); onderweg
      AppProject-destination toegevoegd (least privilege weigerde
      terecht). Eerste sync (handmatig, Mark, 16:43Z) tijdens een
      Codeberg-storing vanaf repo-server-cache: 66 objecten SSA,
      nul wijzigingen, nul pod-restarts; kubectl diff vóór én ná leeg.
      2026-07-11: Synced/Healthy bevestigd; stap 4 (OIDC-rotatie in
      Keycloak + secret-update) door Mark gedaan, SSO-login werkt —
      security-finding afgehandeld
- [ ] 3.2 Observatieperiode; daarna besluit selfHeal aan/uit
- [x] 3.3 Handboek: org-architectuurpagina vermeldt het zelfbeheer — 2026-07-11

## 4. Verify & archive

- [ ] 4.1 Scenario's uit de spec-delta aantonen
- [ ] 4.2 Archive this change
