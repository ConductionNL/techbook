#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Mechanical checks for the docs contract (docs/conventies.md).

Checks per repo: /docs present in root, index.md present, CODEOWNERS
present, and per markdown page a front-matter block with a valid
last_reviewed ISO date and a non-empty owner. Across all repos it lists
duplicate-content candidates (fuzzy match on section heading + opening
paragraph); the list needs human judgement.

Plain text output, no colours. Exit 0 = no findings, 1 = findings,
2 = usage error.

Usage:
  uv run scripts/check_docs_contract.py <repo-path> [<repo-path> ...]
"""

import datetime
import difflib
import re
import sys
from pathlib import Path

import yaml

EXCLUDE_PARTS = {".venv", "venv", "node_modules", ".pytest_cache", ".git",
                 "site-packages", ".tox", "dist", "build"}
CODEOWNERS_LOCATIONS = ("CODEOWNERS", ".github/CODEOWNERS",
                        ".forgejo/CODEOWNERS", "docs/CODEOWNERS")
DUP_MIN_PARA_LEN = 200
DUP_RATIO = 0.75


def md_files(docs_dir: Path) -> list[Path]:
    files = []
    for p in sorted(docs_dir.rglob("*.md")):
        if not EXCLUDE_PARTS.intersection(p.parts):
            files.append(p)
    return files


def parse_front_matter(text: str):
    """Return the front-matter dict, or None if there is no block."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    try:
        data = yaml.safe_load(text[4:end])
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


def check_front_matter(fm) -> list[str]:
    problems = []
    if fm is None:
        return ["front-matter ontbreekt"]
    reviewed = fm.get("last_reviewed")
    if reviewed is None:
        problems.append("last_reviewed ontbreekt")
    elif not isinstance(reviewed, datetime.date):
        try:
            datetime.date.fromisoformat(str(reviewed))
        except ValueError:
            problems.append(f"last_reviewed is geen ISO-datum: {reviewed!r}")
    owner = fm.get("owner")
    if owner is None or str(owner).strip() == "":
        problems.append("owner ontbreekt of is leeg")
    return problems


def sections(text: str):
    """Yield (heading, normalized opening paragraph) per markdown section."""
    current_heading = "(top)"
    buf: list[str] = []
    for line in text.splitlines():
        if line.startswith("#"):
            if buf:
                yield current_heading, " ".join(buf)
            current_heading = line.lstrip("#").strip().lower()
            buf = []
        elif line.strip():
            if buf or not line.startswith(("    ", "\t", "```")):
                buf.append(re.sub(r"\s+", " ", line.strip().lower()))
        elif buf:
            yield current_heading, " ".join(buf)
            buf = []
    if buf:
        yield current_heading, " ".join(buf)


def check_repo(repo: Path) -> list[str]:
    findings = []
    docs = repo / "docs"
    if not docs.is_dir():
        findings.append("/docs ontbreekt in de repo-root")
    else:
        if not (docs / "index.md").is_file():
            findings.append("docs/index.md ontbreekt")
        for page in md_files(docs):
            rel = page.relative_to(repo)
            fm = parse_front_matter(page.read_text(encoding="utf-8",
                                                   errors="replace"))
            for problem in check_front_matter(fm):
                findings.append(f"{rel}: {problem}")
    if not any((repo / loc).is_file() for loc in CODEOWNERS_LOCATIONS):
        findings.append("CODEOWNERS ontbreekt "
                        "(root, .github/, .forgejo/ of docs/)")
    return findings


def duplicate_candidates(repos: list[Path]) -> list[str]:
    entries = []  # (repo_name, rel_path, heading, paragraph)
    for repo in repos:
        docs = repo / "docs"
        if not docs.is_dir():
            continue
        for page in md_files(docs):
            text = page.read_text(encoding="utf-8", errors="replace")
            for heading, para in sections(text):
                if len(para) >= DUP_MIN_PARA_LEN:
                    entries.append((repo.name, page.relative_to(repo),
                                    heading, para))
    candidates = []
    for i, (repo_a, path_a, head_a, para_a) in enumerate(entries):
        for repo_b, path_b, head_b, para_b in entries[i + 1:]:
            if repo_a == repo_b:
                continue
            ratio = difflib.SequenceMatcher(None, para_a, para_b).ratio()
            if ratio >= DUP_RATIO:
                candidates.append(
                    f"{repo_a}/{path_a} '{head_a}' ~ "
                    f"{repo_b}/{path_b} '{head_b}' "
                    f"(overeenkomst {ratio:.0%})")
    return candidates


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    repos = []
    for arg in argv:
        repo = Path(arg).resolve()
        if not repo.is_dir():
            print(f"fout: geen directory: {arg}", file=sys.stderr)
            return 2
        repos.append(repo)

    total = 0
    for repo in repos:
        findings = check_repo(repo)
        docs = repo / "docs"
        pages = len(md_files(docs)) if docs.is_dir() else 0
        print(f"== {repo.name} ({pages} pagina's onder /docs)")
        for finding in findings:
            print(f"   {finding}")
        if not findings:
            print("   geen bevindingen")
        total += len(findings)
        print()

    dups = duplicate_candidates(repos)
    print(f"== duplicaat-kandidaten over repos heen ({len(dups)})")
    for dup in dups:
        print(f"   {dup}")
    if not dups:
        print("   geen")
    total += len(dups)

    print(f"\ntotaal bevindingen: {total}")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
