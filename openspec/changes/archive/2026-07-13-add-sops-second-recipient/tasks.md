# Tasks: add-sops-second-recipient

- [x] 1.1 MENS: 2e age-sleutel gegenereerd + custody belegd (2026-07-13):
      escrow-custodian info@conduction.nl, offline escrow; publieke
      recipient `age13zmwxwgtn86w8fhs28cx90nyp2r8hq9a78p6ufrcer75e9u9j5pszfndpx`
- [x] 1.2 `.sops.yaml`: recipient toegevoegd — in **talos** (de feitelijke
      single-recipient-situatie zat dáár, niet in monitoring) én in
      monitoring (recipientlijst was leeg; stub nu bootstrap-klaar)
- [x] 1.3 MENS: `sops updatekeys` gedraaid en gepusht (2026-07-13,
      talos-commit 42e1215): beide runner-secrets herversleuteld naar
      primair + escrow — monitoring had nog geen echt versleuteld
      bestand
- [x] 1.4 Custody-paragraaf: talos
      `manifests/components/runner-secrets/README.md` + monitoring
      `docs/alerting.md` (incl. stub-status expliciet benoemd)
- [x] 1.5 Besluit talos/monitoring: zelfde sleutelpaar (primair + escrow)
      voor beide repos — één paar volstaat op deze schaal; heroverwegen
      als custody uiteenloopt
- [x] 1.6 Gearchiveerd 2026-07-13
