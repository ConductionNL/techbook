"""Unit- en integratietests voor scripts/check_docs_touched.py.

Het script bestaat om een git-diff te beoordelen; alleen unit-tests zouden
dus liegen. De integratietests draaien op echte tijdelijke repos.

Draaien: uv run --with pytest --with pyyaml --with pathspec \
             python -m pytest tests/ -q
"""

import argparse
import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).parent.parent
SCRIPT = ROOT / "scripts" / "check_docs_touched.py"
spec = importlib.util.spec_from_file_location("cdt", SCRIPT)
cdt = importlib.util.module_from_spec(spec)
sys.modules["cdt"] = cdt
spec.loader.exec_module(cdt)

BASE_CONFIG = {
    "version": 1,
    "mode": "enforce",
    "docs": ["docs/**", "README.md"],
    "rules": [{
        "name": "platform",
        "reason": "platformcode stuurt de runbooks aan",
        "paths": ["nextcloud-platform/**"],
        "exclude": ["**/*.lock"],
    }],
    "ignore": [".github/**"],
    "escape": {"trailer": "Docs-not-needed", "min_reason_len": 10},
}


def write_config(repo: Path, data=None) -> Path:
    path = repo / cdt.CONFIG_NAME
    path.write_text(yaml.safe_dump(data if data is not None else BASE_CONFIG))
    return path


# --- git-helpers voor de integratietests ---------------------------------

def git(repo: Path, *args) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True).stdout


def make_repo(tmp_path, name="repo") -> Path:
    repo = tmp_path / name
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "test@example.org")
    git(repo, "config", "user.name", "test")
    git(repo, "config", "commit.gpgsign", "false")
    return repo


def commit(repo: Path, files: dict, message: str) -> str:
    for rel, content in files.items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD").strip()


def run(repo: Path, from_ref=None, to_ref=None, environ=None, mode=None):
    argv = ["--repo", str(repo)]
    if from_ref:
        argv += ["--from-ref", from_ref, "--to-ref", to_ref or "HEAD"]
    if mode:
        argv += ["--mode", mode]
    return cdt.main(argv, environ={} if environ is None else environ)


# --- pure functies --------------------------------------------------------

class TestMatching:
    def test_nested_globs(self):
        spec_ = cdt.compile_spec(["nextcloud-platform/**"])
        assert cdt.matches(spec_, "nextcloud-platform/a/b/c.yaml")
        assert not cdt.matches(spec_, "andere/a.yaml")

    def test_exclude_wins_from_paths(self):
        hits = cdt.required_paths(
            ["src/a.py", "src/deps.lock"],
            cdt.compile_spec(["src/**"]),
            cdt.compile_spec(["**/*.lock"]),
            cdt.compile_spec([]))
        assert hits == ["src/a.py"]

    def test_ignore_wins_from_both(self):
        hits = cdt.required_paths(
            [".github/workflows/ci.yaml", "src/a.py"],
            cdt.compile_spec(["**"]),
            cdt.compile_spec([]),
            cdt.compile_spec([".github/**"]))
        assert hits == ["src/a.py"]

    def test_docs_detection(self):
        docs_spec = cdt.compile_spec(["docs/**", "README.md"])
        found = cdt.docs_paths(["docs/a/b.md", "README.md", "src/a.py"],
                               docs_spec)
        assert found == ["docs/a/b.md", "README.md"]

    def test_ignore_does_not_hide_docs(self):
        """`ignore` zegt 'vraagt geen docs', niet 'is geen docs'."""
        assert cdt.docs_paths(["docs/a.md"],
                              cdt.compile_spec(["docs/**"])) == ["docs/a.md"]


class TestConfig:
    def test_missing_file_is_skip(self, tmp_path):
        assert cdt.load_config(tmp_path / "bestaat-niet.yaml") is None

    def test_unknown_version_fails_hard(self, tmp_path):
        path = write_config(tmp_path, {**BASE_CONFIG, "version": 99})
        with pytest.raises(cdt.ConfigError):
            cdt.load_config(path)

    def test_missing_version_fails_hard(self, tmp_path):
        data = {k: v for k, v in BASE_CONFIG.items() if k != "version"}
        with pytest.raises(cdt.ConfigError):
            cdt.load_config(write_config(tmp_path, data))

    def test_unknown_mode_fails_hard(self, tmp_path):
        path = write_config(tmp_path, {**BASE_CONFIG, "mode": "misschien"})
        with pytest.raises(cdt.ConfigError):
            cdt.load_config(path)

    def test_rule_without_paths_fails_hard(self, tmp_path):
        data = {**BASE_CONFIG, "rules": [{"name": "x", "paths": []}]}
        with pytest.raises(cdt.ConfigError):
            cdt.load_config(write_config(tmp_path, data))

    def test_defaults_applied(self, tmp_path):
        config = cdt.load_config(write_config(tmp_path, {"version": 1}))
        assert config.mode == cdt.DEFAULT_MODE
        assert config.docs == cdt.DEFAULT_DOCS
        assert config.trailer == cdt.DEFAULT_TRAILER
        assert config.min_reason_len == cdt.DEFAULT_MIN_REASON_LEN

    def test_everything_overridable(self, tmp_path):
        data = {"version": 1, "mode": "enforce", "docs": ["handboek/**"],
                "git_timeout": 5,
                "escape": {"trailer": "Geen-docs", "min_reason_len": 3},
                "report": {"max_files": 2, "max_commits": 1}}
        config = cdt.load_config(write_config(tmp_path, data))
        assert config.trailer == "Geen-docs"
        assert (config.min_reason_len, config.git_timeout) == (3, 5)
        assert (config.max_report_files, config.max_report_commits) == (2, 1)


class TestTrailer:
    def test_valid_reason(self):
        msg = "fix\n\nDocs-not-needed: alleen een typefout in een comment\n"
        assert cdt.valid_exemption(msg, "Docs-not-needed", 10)

    def test_empty_reason_is_no_escape(self):
        assert cdt.valid_exemption("fix\n\nDocs-not-needed:\n",
                                   "Docs-not-needed", 10) is None

    def test_too_short_reason_is_no_escape(self):
        assert cdt.valid_exemption("fix\n\nDocs-not-needed: nvt\n",
                                   "Docs-not-needed", 10) is None

    def test_whitespace_only_reason_is_no_escape(self):
        assert cdt.valid_exemption("fix\n\nDocs-not-needed:       \n",
                                   "Docs-not-needed", 10) is None

    def test_absent_trailer(self):
        assert cdt.valid_exemption("gewoon een commit", "Docs-not-needed",
                                   10) is None

    def test_trailer_name_is_configurable(self):
        msg = "fix\n\nGeen-docs: puur cosmetische wijziging\n"
        assert cdt.valid_exemption(msg, "Geen-docs", 10)


class TestResolveRefs:
    @staticmethod
    def Args(from_ref=None, to_ref=None):
        return argparse.Namespace(from_ref=from_ref, to_ref=to_ref)

    def test_cli_wins(self):
        got = cdt.resolve_refs(self.Args("a", "b"),
                               {"PRE_COMMIT_FROM_REF": "c",
                                "PRE_COMMIT_TO_REF": "d"})
        assert got[:2] == ("a", "b")

    def test_env_then_legacy(self):
        assert cdt.resolve_refs(self.Args(), {
            "PRE_COMMIT_FROM_REF": "c", "PRE_COMMIT_TO_REF": "d"})[:2] \
            == ("c", "d")
        assert cdt.resolve_refs(self.Args(), {
            "PRE_COMMIT_ORIGIN": "e", "PRE_COMMIT_SOURCE": "f"})[:2] \
            == ("e", "f")

    def test_half_pair_is_no_context(self):
        assert cdt.resolve_refs(self.Args(),
                                {"PRE_COMMIT_FROM_REF": "c"}) is None

    def test_nothing_is_no_context(self):
        assert cdt.resolve_refs(self.Args(), {}) is None


# --- integratie op echte repos -------------------------------------------

class TestIntegration:
    def setup_repo(self, tmp_path, config=None):
        repo = make_repo(tmp_path)
        write_config(repo, config)
        base = commit(repo, {"docs/index.md": "# start\n"}, "init")
        return repo, base

    def test_code_only_fails_in_enforce(self, tmp_path, capsys):
        repo, base = self.setup_repo(tmp_path)
        commit(repo, {"nextcloud-platform/values.yaml": "a: 1\n"}, "code")
        assert run(repo, base) == 1
        out = capsys.readouterr().out
        assert "platform" in out and "runbooks" in out

    def test_code_plus_docs_passes(self, tmp_path):
        repo, base = self.setup_repo(tmp_path)
        commit(repo, {"nextcloud-platform/values.yaml": "a: 1\n",
                      "docs/platform.md": "# uitleg\n"}, "code+docs")
        assert run(repo, base) == 0

    def test_docs_in_later_commit_passes(self, tmp_path):
        """Docs-as-code geldt per push, niet per losse commit."""
        repo, base = self.setup_repo(tmp_path)
        commit(repo, {"nextcloud-platform/values.yaml": "a: 1\n"}, "code")
        commit(repo, {"docs/platform.md": "# uitleg\n"}, "docs achteraf")
        assert run(repo, base) == 0

    def test_docs_only_passes(self, tmp_path):
        repo, base = self.setup_repo(tmp_path)
        commit(repo, {"docs/uitleg.md": "# uitleg\n"}, "alleen docs")
        assert run(repo, base) == 0

    def test_path_outside_config_passes(self, tmp_path):
        repo, base = self.setup_repo(tmp_path)
        commit(repo, {"tools/script.sh": "echo hoi\n"}, "buiten scope")
        assert run(repo, base) == 0

    def test_excluded_path_passes(self, tmp_path):
        repo, base = self.setup_repo(tmp_path)
        commit(repo, {"nextcloud-platform/deps.lock": "x\n"}, "lockfile")
        assert run(repo, base) == 0

    def test_ignored_path_passes(self, tmp_path):
        repo, base = self.setup_repo(tmp_path)
        commit(repo, {".github/workflows/ci.yaml": "on: push\n"}, "ci")
        assert run(repo, base) == 0

    def test_warn_mode_reports_but_exits_zero(self, tmp_path, capsys):
        repo, base = self.setup_repo(tmp_path,
                                     {**BASE_CONFIG, "mode": "warn"})
        commit(repo, {"nextcloud-platform/values.yaml": "a: 1\n"}, "code")
        assert run(repo, base) == 0
        out = capsys.readouterr().out
        assert "geschonden" in out and "mode warn" in out

    def test_trailer_exempts_only_its_own_commit(self, tmp_path, capsys):
        repo, base = self.setup_repo(tmp_path)
        commit(repo, {"nextcloud-platform/a.yaml": "a: 1\n"},
               "vrijgesteld\n\nDocs-not-needed: alleen witruimte opgeschoond")
        commit(repo, {"nextcloud-platform/b.yaml": "b: 2\n"}, "gewone commit")
        assert run(repo, base) == 1
        out = capsys.readouterr().out
        assert "vrijgesteld" in out
        assert "nextcloud-platform/b.yaml" in out
        assert "nextcloud-platform/a.yaml" not in out

    def test_trailer_on_every_commit_passes(self, tmp_path):
        repo, base = self.setup_repo(tmp_path)
        commit(repo, {"nextcloud-platform/a.yaml": "a: 1\n"},
               "een\n\nDocs-not-needed: alleen witruimte opgeschoond")
        commit(repo, {"nextcloud-platform/b.yaml": "b: 2\n"},
               "twee\n\nDocs-not-needed: alleen witruimte opgeschoond")
        assert run(repo, base) == 0

    def test_short_trailer_reason_does_not_exempt(self, tmp_path):
        repo, base = self.setup_repo(tmp_path)
        commit(repo, {"nextcloud-platform/a.yaml": "a: 1\n"},
               "een\n\nDocs-not-needed: nee")
        assert run(repo, base) == 1

    def test_merge_commit_counted_once(self, tmp_path, capsys):
        repo, base = self.setup_repo(tmp_path)
        git(repo, "checkout", "-q", "-b", "zijtak")
        commit(repo, {"nextcloud-platform/values.yaml": "a: 1\n"}, "code")
        git(repo, "checkout", "-q", "main")
        commit(repo, {"tools/x.sh": "echo\n"}, "los werk")
        git(repo, "merge", "-q", "--no-ff", "-m", "merge zijtak", "zijtak")
        assert run(repo, base) == 1
        out = capsys.readouterr().out
        assert out.count("gewijzigd: nextcloud-platform/values.yaml") == 1

    def test_new_branch_without_upstream(self, tmp_path):
        """Pre-commit levert dan `<first_ancestor>^` als from_ref."""
        repo, base = self.setup_repo(tmp_path)
        git(repo, "checkout", "-q", "-b", "feature")
        first = commit(repo, {"nextcloud-platform/values.yaml": "a: 1\n"},
                       "eerste op de tak")
        commit(repo, {"nextcloud-platform/meer.yaml": "b: 2\n"}, "tweede")
        from_ref = git(repo, "rev-parse", f"{first}^").strip()
        assert run(repo, from_ref) == 1

    def test_no_refs_is_skip(self, tmp_path, capsys):
        repo, _ = self.setup_repo(tmp_path)
        commit(repo, {"nextcloud-platform/values.yaml": "a: 1\n"}, "code")
        assert run(repo) == 0
        assert "geen diff-context" in capsys.readouterr().out

    def test_root_commit_range_works(self, tmp_path):
        """Root-commit als from_ref: de eerste commit zelf telt niet mee."""
        repo, base = self.setup_repo(tmp_path)
        commit(repo, {"nextcloud-platform/values.yaml": "a: 1\n"}, "code")
        root = git(repo, "rev-list", "--max-parents=0", "HEAD").strip()
        assert root == base
        assert run(repo, root) == 1

    def test_missing_config_is_skip(self, tmp_path, capsys):
        repo = make_repo(tmp_path)
        base = commit(repo, {"docs/index.md": "# start\n"}, "init")
        commit(repo, {"nextcloud-platform/values.yaml": "a: 1\n"}, "code")
        assert run(repo, base) == 0
        assert "overgeslagen" in capsys.readouterr().out

    def test_broken_config_exits_two(self, tmp_path):
        repo, base = self.setup_repo(tmp_path, {**BASE_CONFIG, "version": 42})
        assert run(repo, base) == 2

    def test_vanished_from_ref_degrades(self, tmp_path, capsys):
        repo, _ = self.setup_repo(tmp_path)
        commit(repo, {"nextcloud-platform/values.yaml": "a: 1\n"}, "code")
        gone = "0" * 40
        assert run(repo, gone) == 0
        out = capsys.readouterr().out
        assert "kon diff niet bepalen" in out
        assert "Traceback" not in out

    def test_env_refs_are_used(self, tmp_path):
        repo, base = self.setup_repo(tmp_path)
        commit(repo, {"nextcloud-platform/values.yaml": "a: 1\n"}, "code")
        assert cdt.main(["--repo", str(repo)],
                        environ={"PRE_COMMIT_FROM_REF": base,
                                 "PRE_COMMIT_TO_REF": "HEAD"}) == 1

    def test_rule_docs_stricter_than_global(self, tmp_path):
        config = {**BASE_CONFIG, "rules": [{
            "name": "platform",
            "reason": "runbooks",
            "paths": ["nextcloud-platform/**"],
            "docs": ["docs/platform/**"]}]}
        repo, base = self.setup_repo(tmp_path, config)
        commit(repo, {"nextcloud-platform/values.yaml": "a: 1\n",
                      "docs/algemeen.md": "# iets\n"}, "verkeerde docs")
        assert run(repo, base) == 1
        commit(repo, {"docs/platform/uitleg.md": "# uitleg\n"}, "juiste docs")
        assert run(repo, base) == 0

    def test_mode_flag_overrides_config(self, tmp_path):
        repo, base = self.setup_repo(tmp_path,
                                     {**BASE_CONFIG, "mode": "warn"})
        commit(repo, {"nextcloud-platform/values.yaml": "a: 1\n"}, "code")
        assert run(repo, base) == 0
        assert run(repo, base, mode="enforce") == 1


# --- vormtest op de geëxporteerde hookdefinitie ---------------------------

class TestHookDefinition:
    def test_docs_touched_is_wired_correctly(self):
        hooks = yaml.safe_load((ROOT / ".pre-commit-hooks.yaml").read_text())
        hook = next(h for h in hooks if h["id"] == "docs-touched")
        assert hook["entry"] == "scripts/check_docs_touched.py"
        assert hook["language"] == "script"
        assert hook["stages"] == ["pre-push"]
        assert hook["always_run"] is True
        assert hook["pass_filenames"] is False
        assert "args" not in hook

    def test_own_config_is_parseable(self):
        config = cdt.load_config(ROOT / cdt.CONFIG_NAME)
        assert config is not None and config.mode in cdt.MODES
