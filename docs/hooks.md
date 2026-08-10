---
last_reviewed: 2026-08-10
owner: info@conduction.nl
---

# Hookset en pin-beheer

Techbook exporteert de gedeelde pre-push gates; elke deelnemende repo
consumeert ze via een **sha-pin** in `.pre-commit-config.yaml`. Dit is
de referentie voor wat er draait en hoe je de pin bumpt.

## De hookset per repo

| Hook | Bron | Doet |
|---|---|---|
| `docs-contract` | techbook (pin) | front-matter, index.md, CODEOWNERS |
| `docs-claims` | techbook (pin) | uitvoerbare `verify`-docs-blokken |
| `verify` | lokaal (`scripts/verify.sh`) | unit tests / dry-runs / doc-assertions |
| `gitleaks` | gitleaks/gitleaks (v8.18.4) | secret-scanning |
| `detect-private-key` | pre-commit-hooks (v4.6.0) | private keys |

Nieuwe repo? `scripts/rollout_precommit_hook.sh --rev <sha> <pad>`
schrijft dit geheel en installeert de hook.

Techbook exporteert daarnaast [`docs-touched`](docs-touched.md), de
diff-gate op docs-as-code. Die staat **nog niet** in de consumer-configs:
uitrollen is een aparte stap (rev-bump plus een `.docs-touched.yaml` per
repo) die pas kan nadat deze hook in techbook-main zit.

## Pin bumpen (procedure)

De techbook-sha staat gedupliceerd in álle consumer-configs; bump hem
alleen als een gedeelde hook wijzigt, en altijd zo:

1. Wijziging in techbook committen; **pushen** (de pin moet remote
   bestaan vóór welke consumer-push dan ook).
2. Nieuwe sha: `git -C techbook rev-parse HEAD`.
3. In alle consumers: `rev:` vervangen (sed over
   `.pre-commit-config.yaml`), per repo committen.
4. Keten valideren in mínstens één repo:
   `pre-commit run docs-contract --hook-stage pre-push --all-files`.
5. Consumers pushen. Wie bumpt: degene die de hook wijzigde;
   volgorde is heilig (techbook eerst), anders faalt elke push op een
   onvindbare pin.

Automatiseringsvoorstel (niet gebouwd): een techbook-script dat stap
3–4 doet; afwegen zodra bumps vaker dan maandelijks voorkomen.

## Waarom sha-pins

Consumers draaien gate-code uit techbook; een pin maakt dat
reproduceerbaar en reviewbaar (welke code draaide bij welke push), en
voorkomt dat een push naar techbook-main stilzwijgend gedrag wijzigt
in elke repo — zelfde trust-root-gedachte als de handbook-importlijst.
