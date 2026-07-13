# Change: add-sops-second-recipient

## Why

De age-key waarmee monitoring-secrets (Slack-webhook) zijn versleuteld
heeft één recipient en één custodian: bus-factor 1, geen escrow, geen
vastgelegd rotatiepad (review-bevinding WP4, 2026-07-10).

## What Changes

- `.sops.yaml` in monitoring krijgt een tweede age-recipient
  (team-/escrow-sleutel); bestaande `*.sops.yaml` worden ge-updatekeyed.
- Custody-paragraaf in monitoring docs: waar leven de private keys, wie
  houdt ze, hoe roteren.
- MENSENWERK (agent raakt nooit key-materiaal): sleutel genereren
  (`age-keygen`), veilig opslaan (2e custodian + offline escrow),
  daarna per bestand `sops updatekeys <f>.sops.yaml` en committen.

## Non-goals

- Geen migratie naar Vault/ESO in deze change (staat al als deferred in
  talos/monitoring-docs).

## Impact

- Affected repos: monitoring (en het patroon is herbruikbaar voor talos'
  runner-secrets — aparte opvolging)
- Risk: laag — updatekeys herversleutelt; de oude key blijft werken tot
  bewust verwijderd
