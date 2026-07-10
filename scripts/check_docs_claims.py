#!/usr/bin/env python3
"""Uitvoerbare documentatie (spec docs-claims): draai verify-blokken.

Extraheert fenced codeblocks waarvan de info-string het woord `verify`
bevat (```bash verify) uit markdown-bomen en voert ze uit als dry-run:
bash met -euo pipefail, timeout, zonder cluster-credentials
(KUBECONFIG wordt geleegd). Dekking is zichtbaar: elke pagina wordt
gerapporteerd, ook met 0 claims.

Alleen bash/sh-blokken worden ondersteund; een verify-blok in een
andere taal faalt luid (nooit stil overslaan). Exit 0 = alle claims
groen, 1 = falende/onondersteunde claim, 2 = aanroepfout.

Usage:
  scripts/check_docs_claims.py docs
  scripts/check_docs_claims.py docs --timeout 30
"""

import argparse
import os
import pathlib
import re
import subprocess
import sys

EXCLUDE_PARTS = {".venv", "venv", "node_modules", ".pytest_cache", ".git",
                 "site-packages", "site", "multirepo_imports"}
FENCE_RE = re.compile(r"^(```+|~~~+)\s*(\S*)\s*(.*)$")
SUPPORTED = {"bash", "sh", "shell"}


def md_files(root: pathlib.Path):
    for p in sorted(root.rglob("*.md")):
        if not EXCLUDE_PARTS.intersection(p.parts):
            yield p


def extract_blocks(text: str):
    """Yield (language, marker_ok, code) voor elk verify-gemarkeerd blok."""
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = FENCE_RE.match(lines[i])
        if m and "verify" in m.group(3).split():
            fence, lang = m.group(1), m.group(2).lower()
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith(fence):
                code.append(lines[i])
                i += 1
            yield lang, lang in SUPPORTED, "\n".join(code)
        i += 1


def run_block(code: str, cwd: pathlib.Path, timeout: int):
    """Draai één blok; return (ok, detail)."""
    env = dict(os.environ)
    env["KUBECONFIG"] = "/dev/null"     # nooit per ongeluk een cluster
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        result = subprocess.run(
            ["bash", "-euo", "pipefail", "-c", code],
            cwd=cwd, env=env, capture_output=True, text=True,
            timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, f"timeout na {timeout}s"
    if result.returncode != 0:
        tail = (result.stderr or result.stdout).strip().splitlines()[-3:]
        return False, f"exit {result.returncode}: " + " | ".join(tail)
    return True, ""


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Draai verify-gemarkeerde docs-codeblokken als gate.")
    parser.add_argument("roots", nargs="+")
    parser.add_argument("--timeout", type=int, default=60,
                        help="seconden per blok (default 60)")
    args = parser.parse_args(argv)

    repo_root = pathlib.Path.cwd()
    failures = 0
    total_claims = 0
    zero_pages = []
    for root_arg in args.roots:
        root = pathlib.Path(root_arg)
        if not root.is_dir():
            print(f"fout: geen directory: {root_arg}", file=sys.stderr)
            return 2
        for page in md_files(root):
            blocks = list(extract_blocks(
                page.read_text(encoding="utf-8", errors="replace")))
            if not blocks:
                zero_pages.append(str(page))
                continue
            for n, (lang, supported, code) in enumerate(blocks, 1):
                total_claims += 1
                if not supported:
                    print(f"FAAL {page} blok {n}: taal {lang!r} niet "
                          "ondersteund voor verify-blokken")
                    failures += 1
                    continue
                ok, detail = run_block(code, repo_root, args.timeout)
                status = "OK  " if ok else "FAAL"
                print(f"{status} {page} blok {n}"
                      + (f": {detail}" if detail else ""))
                failures += 0 if ok else 1

    print(f"\nclaims: {total_claims} getoetst, {failures} gefaald; "
          f"pagina's zonder claims: {len(zero_pages)}")
    for p in zero_pages:
        print(f"  0 claims: {p}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
