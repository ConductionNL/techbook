"""Unit tests voor scripts/check_docs_contract.py.

Draaien: uv run --with pytest --with pyyaml python -m pytest tests/ -q
"""

import importlib.util
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "check_docs_contract.py"
spec = importlib.util.spec_from_file_location("cdc", SCRIPT)
cdc = importlib.util.module_from_spec(spec)
sys.modules["cdc"] = cdc
spec.loader.exec_module(cdc)

VALID_FM = "---\nlast_reviewed: 2026-07-06\nowner: mark\n---\n\n# Titel\n"


def make_repo(tmp_path, name="repo", pages=None, codeowners=True, index=True):
    repo = tmp_path / name
    docs = repo / "docs"
    docs.mkdir(parents=True)
    if index:
        (docs / "index.md").write_text(VALID_FM)
    for rel, content in (pages or {}).items():
        p = docs / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)
    if codeowners:
        (repo / "CODEOWNERS").write_text("docs/ @mark\n")
    return repo


class TestParseFrontMatter:
    def test_valid(self):
        fm = cdc.parse_front_matter(VALID_FM)
        assert fm["owner"] == "mark"

    def test_missing_block(self):
        assert cdc.parse_front_matter("# Gewoon een titel\n") is None

    def test_unterminated_block(self):
        assert cdc.parse_front_matter("---\nowner: mark\n") is None

    def test_invalid_yaml(self):
        assert cdc.parse_front_matter("---\n: [::\n---\n") is None


class TestCheckFrontMatter:
    def test_valid_passes(self):
        assert cdc.check_front_matter({"last_reviewed": "2026-07-06",
                                       "owner": "mark"}) == []

    def test_missing_front_matter(self):
        assert cdc.check_front_matter(None) == ["front-matter ontbreekt"]

    def test_missing_last_reviewed(self):
        problems = cdc.check_front_matter({"owner": "mark"})
        assert any("last_reviewed" in p for p in problems)

    def test_bad_date(self):
        problems = cdc.check_front_matter({"last_reviewed": "volgende week",
                                           "owner": "mark"})
        assert any("ISO-datum" in p for p in problems)

    def test_empty_owner(self):
        problems = cdc.check_front_matter({"last_reviewed": "2026-07-06",
                                           "owner": " "})
        assert any("owner" in p for p in problems)


class TestCheckRepo:
    def test_clean_repo(self, tmp_path):
        repo = make_repo(tmp_path, pages={"a.md": VALID_FM})
        assert cdc.check_repo(repo) == []

    def test_missing_docs_dir(self, tmp_path):
        repo = tmp_path / "leeg"
        repo.mkdir()
        findings = cdc.check_repo(repo)
        assert any("/docs ontbreekt" in f for f in findings)
        assert any("CODEOWNERS" in f for f in findings)

    def test_missing_index_and_codeowners(self, tmp_path):
        repo = make_repo(tmp_path, index=False, codeowners=False)
        findings = cdc.check_repo(repo)
        assert any("index.md" in f for f in findings)
        assert any("CODEOWNERS" in f for f in findings)

    def test_page_without_front_matter(self, tmp_path):
        repo = make_repo(tmp_path, pages={"kaal.md": "# Geen front-matter\n"})
        assert any("kaal.md" in f for f in cdc.check_repo(repo))

    def test_codeowners_alternative_locations(self, tmp_path):
        repo = make_repo(tmp_path, codeowners=False)
        (repo / ".github").mkdir()
        (repo / ".github" / "CODEOWNERS").write_text("docs/ @mark\n")
        assert cdc.check_repo(repo) == []

    def test_vendored_paths_excluded(self, tmp_path):
        repo = make_repo(tmp_path)
        venv = repo / "docs" / ".venv" / "lib"
        venv.mkdir(parents=True)
        (venv / "vendored.md").write_text("# Zonder front-matter\n")
        assert cdc.check_repo(repo) == []


class TestDuplicateCandidates:
    PARA = ("Deze installatie-instructie beschrijft stap voor stap hoe je de "
            "omgeving opzet met kubectl, de juiste namespace aanmaakt en de "
            "secrets versleutelt met sops en age voordat argo cd gaat syncen "
            "en de applicatie beschikbaar wordt op het cluster.")

    def test_cross_repo_duplicate_found(self, tmp_path):
        page = VALID_FM + "\n## Setup\n\n" + self.PARA + "\n"
        a = make_repo(tmp_path, "repo-a", pages={"setup.md": page})
        b = make_repo(tmp_path, "repo-b", pages={"install.md": page})
        assert len(cdc.duplicate_candidates([a, b])) == 1

    def test_same_repo_not_reported(self, tmp_path):
        page = VALID_FM + "\n## Setup\n\n" + self.PARA + "\n"
        a = make_repo(tmp_path, "repo-a",
                      pages={"x.md": page, "y.md": page})
        assert cdc.duplicate_candidates([a]) == []

    def test_short_sections_ignored(self, tmp_path):
        page = VALID_FM + "\n## Kort\n\nTe kort om te tellen.\n"
        a = make_repo(tmp_path, "repo-a", pages={"x.md": page})
        b = make_repo(tmp_path, "repo-b", pages={"y.md": page})
        assert cdc.duplicate_candidates([a, b]) == []


class TestMain:
    def test_exit_zero_on_clean_repo(self, tmp_path, capsys):
        repo = make_repo(tmp_path, pages={"a.md": VALID_FM})
        assert cdc.main([str(repo)]) == 0
        assert "geen bevindingen" in capsys.readouterr().out

    def test_exit_one_on_findings(self, tmp_path, capsys):
        repo = make_repo(tmp_path, index=False)
        assert cdc.main([str(repo)]) == 1
        assert "totaal bevindingen: 1" in capsys.readouterr().out

    def test_exit_two_on_bad_path(self, tmp_path):
        assert cdc.main([str(tmp_path / "bestaat-niet")]) == 2
