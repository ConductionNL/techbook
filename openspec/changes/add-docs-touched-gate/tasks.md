# Tasks: add-docs-touched-gate

## 1. Gate

- [x] 1.1 `scripts/check_docs_touched.py`: ref-resolutie met precedentie
      CLI → `PRE_COMMIT_FROM_REF/TO_REF` → legacy `PRE_COMMIT_ORIGIN/
      SOURCE` → zichtbare overslag; nooit een baseline raden
- [x] 1.2 Diff via `<from>...<to>` met terugval op `..` (conventie uit
      `pre_commit/git.py`); verdwenen `from_ref` degradeert naar exit 0
      met een melding, geen traceback
- [x] 1.3 Configlezer `.docs-touched.yaml`: onbekende/ontbrekende
      `version` faalt hard, ontbrekend bestand is een zichtbare overslag
- [x] 1.4 Matching via `pathspec` (gitignore-semantiek), precedentie
      `ignore` > `exclude` > `paths`; `ignore` verbergt géén docs
- [x] 1.5 Vrijstelling per commit via de trailer, met minimale
      redenlengte; merges tellen niet dubbel
- [x] 1.6 Foutmelding toont refs, bestandsaantal, regel + reden, de
      betrokken commits en een `git fetch`-hint bij een te brede diff

## 2. Inbedding

- [x] 2.1 `docs-touched` in `.pre-commit-hooks.yaml` (pre-push,
      `always_run`, `pass_filenames: false`, géén `args:`)
- [x] 2.2 Dogfooding: hook + `.docs-touched.yaml` (`mode: warn`) in
      techbook zelf
- [x] 2.3 `tests`-hook aangevuld met `--with pathspec`

## 3. Tests

- [x] 3.1 Pure functies: matching/precedentie, configvalidatie,
      trailerafhandeling, ref-resolutie
- [x] 3.2 Integratie op echte tijdelijke git-repos: alleen-code,
      code+docs, docs in een latere commit, alleen-docs, buiten scope,
      warn vs enforce, trailer stelt alleen zijn eigen commit vrij,
      nieuwe tak zonder upstream, root-commit, merge telt niet dubbel,
      verdwenen ref, ontbrekende config
- [x] 3.3 Vormtest op `.pre-commit-hooks.yaml` (een typo in `stages` is
      anders volledig stil)

## 4. Documentatie

- [x] 4.1 `docs/docs-touched.md` met configformaat, vrijstelling en een
      `verify`-blok
- [x] 4.2 `docs/conventies.md` §7 en §Naleving benoemen het mechanisme
- [x] 4.3 `docs/index.md` en `docs/hooks.md` bijgewerkt
- [x] 4.4 CHANGELOG-regel

## 5. Uitrol (buiten deze change)

- [ ] 5.1 Mens: techbook mergen en de sha vastleggen
- [ ] 5.2 Rev-bump in de consumers plus per repo een `.docs-touched.yaml`
      in `mode: warn`; `rollout_precommit_hook.sh` schrijft
      `.pre-commit-config.yaml` in zijn geheel, dus de padlijsten horen
      daar niet in
- [ ] 5.3 Hookbron van Codeberg naar GitHub (de repos zijn verhuisd;
      `HOOK_REPO_URL` in `rollout_precommit_hook.sh` wijst nog naar
      Codeberg)
- [ ] 5.4 Omzetdatum naar `enforce` per repo vastleggen
- [ ] 5.5 Dezelfde §7-tekst in de canonieke `handbook`
      `docs/org/conventies.md` bijwerken (techbook heeft alleen een kopie)
- [ ] 5.6 Change archiveren
