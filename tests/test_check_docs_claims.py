"""Unit tests voor scripts/check_docs_claims.py.

Draaien: uv run --with pytest python -m pytest tests/test_check_docs_claims.py -q
"""

import importlib.util
import os
import pathlib
import sys

SCRIPT = pathlib.Path(__file__).parent.parent / "scripts" / "check_docs_claims.py"
spec = importlib.util.spec_from_file_location("cdc2", SCRIPT)
cdc = importlib.util.module_from_spec(spec)
sys.modules["cdc2"] = cdc
spec.loader.exec_module(cdc)


def page(tmp_path, name, body):
    docs = tmp_path / "docs"
    docs.mkdir(exist_ok=True)
    (docs / name).write_text(body)
    return docs


def run_main(tmp_path, docs, capsys, **kw):
    olddir = os.getcwd()
    os.chdir(tmp_path)
    try:
        code = cdc.main([str(docs.relative_to(tmp_path))] + kw.get("extra", []))
    finally:
        os.chdir(olddir)
    return code, capsys.readouterr().out


class TestExtract:
    def test_marked_block_found(self):
        blocks = list(cdc.extract_blocks(
            "tekst\n```bash verify\necho hoi\n```\n"))
        assert blocks == [("bash", True, "echo hoi")]

    def test_unmarked_block_ignored(self):
        assert list(cdc.extract_blocks("```bash\necho nee\n```\n")) == []

    def test_unsupported_language_flagged(self):
        blocks = list(cdc.extract_blocks("```python verify\nprint(1)\n```\n"))
        assert blocks[0][1] is False


class TestRun:
    def test_passing_claim(self, tmp_path, capsys):
        docs = page(tmp_path, "a.md", "```bash verify\ntrue\n```\n")
        code, out = run_main(tmp_path, docs, capsys)
        assert code == 0
        assert "claims: 1 getoetst, 0 gefaald" in out

    def test_failing_claim_blocks(self, tmp_path, capsys):
        docs = page(tmp_path, "a.md", "```bash verify\nfalse\n```\n")
        code, out = run_main(tmp_path, docs, capsys)
        assert code == 1
        assert "FAAL" in out

    def test_unsupported_language_fails_loud(self, tmp_path, capsys):
        docs = page(tmp_path, "a.md", "```python verify\nprint(1)\n```\n")
        code, out = run_main(tmp_path, docs, capsys)
        assert code == 1
        assert "niet ondersteund" in out

    def test_zero_claim_page_visible(self, tmp_path, capsys):
        docs = page(tmp_path, "proza.md", "# Alleen uitleg\n")
        code, out = run_main(tmp_path, docs, capsys)
        assert code == 0
        assert "0 claims: docs/proza.md" in out

    def test_timeout_fails(self, tmp_path, capsys):
        docs = page(tmp_path, "a.md", "```bash verify\nsleep 5\n```\n")
        code, out = run_main(tmp_path, docs, capsys,
                             extra=["--timeout", "1"])
        assert code == 1
        assert "timeout" in out

    def test_kubeconfig_neutralised(self, tmp_path, capsys, monkeypatch):
        monkeypatch.setenv("KUBECONFIG", "/echt/bestaand/config")
        docs = page(tmp_path, "a.md",
                    '```bash verify\ntest "$KUBECONFIG" = /dev/null\n```\n')
        code, _ = run_main(tmp_path, docs, capsys)
        assert code == 0
