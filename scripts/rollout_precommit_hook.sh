#!/usr/bin/env bash
# SPDX-License-Identifier: EUPL-1.2
# role: tool
#
# scripts/rollout_precommit_hook.sh — rol de docs-contract pre-push hook uit
# naar deelnemende repos.
#
# Schrijft per repo een .pre-commit-config.yaml die techbooks `docs-contract`
# hook consumeert (gepind op een sha/tag), commit die, en activeert de hook
# met `pre-commit install --hook-type pre-push`. Repos met een bestaande
# .pre-commit-config.yaml zonder techbook-entry worden overgeslagen met een
# waarschuwing (geen auto-merge van andermans config — gate, geen fix).
#
# Writes: <repo>/.pre-commit-config.yaml + één git-commit per repo (geen push)
# Idempotent: ja — al geconfigureerde repos worden overgeslagen
# Requires: git, pre-commit; de opgegeven rev moet op Codeberg gepusht zijn
#           vóór de eerste echte pre-push run (pre-commit clonet techbook)
#
# Usage:
#   ./scripts/rollout_precommit_hook.sh --rev <sha-of-tag> --all
#   ./scripts/rollout_precommit_hook.sh --rev <sha-of-tag> ~/CONDUCTION/talos
#   REPO_ROOT=~/CONDUCTION ./scripts/rollout_precommit_hook.sh --rev v0.1.0 --all

set -euo pipefail

readonly HOOK_REPO_URL="https://codeberg.org/Conduction/techbook"
readonly REPO_ROOT="${REPO_ROOT:-$HOME/CONDUCTION}"
readonly ALL_REPOS=(react-base Nextcloud-base cluster-infra KeyCloak talos
                    cluster-config monitoring openwoo-app-config)

usage() {
  sed -n '5,23p' "$0" >&2
  exit 2
}

log() { echo "$*"; }
warn() { echo "waarschuwing: $*" >&2; }

write_config() {
  local repo_dir="$1" rev="$2"
  cat > "${repo_dir}/.pre-commit-config.yaml" <<EOF
# Gate-mode hooks (nooit auto-fix). Activeren:
#   pre-commit install --hook-type pre-push
repos:
  - repo: ${HOOK_REPO_URL}
    rev: ${rev}
    hooks:
      - id: docs-contract
EOF
}

rollout_repo() {
  local repo_dir="$1" rev="$2" name
  name="$(basename "${repo_dir}")"

  if [[ ! -d "${repo_dir}/.git" ]]; then
    warn "${name}: geen git-repo, overgeslagen"
    return 1
  fi

  local config="${repo_dir}/.pre-commit-config.yaml"
  if [[ -f "${config}" ]]; then
    if grep -q "${HOOK_REPO_URL}" "${config}"; then
      log "${name}: al geconfigureerd — alleen hook (her)installeren"
    else
      warn "${name}: bestaande .pre-commit-config.yaml zonder techbook-entry;"
      warn "${name}: voeg de docs-contract hook handmatig toe (zie usage-blok)"
      return 1
    fi
  else
    write_config "${repo_dir}" "${rev}"
    git -C "${repo_dir}" add .pre-commit-config.yaml
    git -C "${repo_dir}" commit --quiet -m \
      "chore: docs-contract pre-push gate via techbook hook"
    log "${name}: config geschreven en gecommit"
  fi

  (cd "${repo_dir}" && pre-commit install --hook-type pre-push >/dev/null)
  log "${name}: pre-push hook geïnstalleerd"
}

main() {
  local rev="" use_all=false
  local -a repos=()

  while (($# > 0)); do
    case "$1" in
      --rev) rev="${2:?--rev vereist een waarde}"; shift 2 ;;
      --all) use_all=true; shift ;;
      -h|--help) usage ;;
      *) repos+=("$1"); shift ;;
    esac
  done

  [[ -n "${rev}" ]] || { warn "--rev <sha-of-tag> is verplicht"; usage; }
  if "${use_all}"; then
    local r
    for r in "${ALL_REPOS[@]}"; do repos+=("${REPO_ROOT}/${r}"); done
  fi
  ((${#repos[@]} > 0)) || { warn "geen repos opgegeven"; usage; }

  command -v pre-commit >/dev/null || {
    warn "pre-commit niet gevonden (pip install --user pre-commit)"; exit 1; }

  local failures=0 repo
  for repo in "${repos[@]}"; do
    rollout_repo "${repo}" "${rev}" || failures=$((failures + 1))
  done

  log ""
  log "klaar: $((${#repos[@]} - failures))/${#repos[@]} repos geconfigureerd"
  ((failures == 0)) || exit 1
}

main "$@"
