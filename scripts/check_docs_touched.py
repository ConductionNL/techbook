#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml", "pathspec>=0.12,<2"]
# ///
"""Diff-gate op docs-as-code (docs/conventies.md §7).

Kijkt naar de commits die daadwerkelijk gepusht worden en faalt wanneer
docs-plichtige paden wijzigen zonder dat er documentatie meeverandert.
De regels staan in `.docs-touched.yaml` in de repo-root, niet in
`args:` van `.pre-commit-config.yaml` (dat bestand wordt door
scripts/rollout_precommit_hook.sh in zijn geheel herschreven).

Twee hendels die een uitrol over meerdere repos veilig maken: zonder
diff-context (geen refs) en zonder configbestand slaat de hook zichzelf
*zichtbaar* over met exit 0. Raden naar een baseline gebeurt nooit — een
gate die stiekem het verkeerde meet is erger dan geen gate.

Vrijstelling is per commit, via de trailer `Docs-not-needed: <reden>`.
Een vrijgestelde commit draagt geen eis bij; de overige commits wel.

Plain text output, geen kleuren. Exit 0 = akkoord of overgeslagen,
1 = bevindingen in mode `enforce`, 2 = config-/aanroepfout.

Usage:
  scripts/check_docs_touched.py
  scripts/check_docs_touched.py --from-ref origin/main --to-ref HEAD
  scripts/check_docs_touched.py --config .docs-touched.yaml --mode enforce
  PRE_COMMIT_FROM_REF=abc PRE_COMMIT_TO_REF=def scripts/check_docs_touched.py
"""

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass, field, replace
from pathlib import Path

import pathspec
import yaml

# Defaults. Alles hieronder is via .docs-touched.yaml te overschrijven;
# er zit met opzet geen drempel of patroon vast in de code.
CONFIG_NAME = ".docs-touched.yaml"
SUPPORTED_VERSIONS = (1,)
MODES = ("warn", "enforce")
DEFAULT_MODE = "warn"
DEFAULT_DOCS = ("docs/**", "README.md")
DEFAULT_IGNORE = ()
DEFAULT_TRAILER = "Docs-not-needed"
DEFAULT_MIN_REASON_LEN = 10
DEFAULT_GIT_TIMEOUT = 60
DEFAULT_MAX_REPORT_FILES = 20
DEFAULT_MAX_REPORT_COMMITS = 10

# Env-namen die pre-commit zet; alleen als from én to truthy zijn
# (pre_commit/commands/run.py). Volgorde = precedentie.
ENV_REF_PAIRS = (("PRE_COMMIT_FROM_REF", "PRE_COMMIT_TO_REF"),
                 ("PRE_COMMIT_ORIGIN", "PRE_COMMIT_SOURCE"))

PREFIX = "docs-touched:"


class ConfigError(Exception):
    """Onbruikbare of niet-ondersteunde .docs-touched.yaml."""


class GitError(Exception):
    """Git kon de gevraagde diff niet leveren."""


@dataclass(frozen=True)
class Rule:
    name: str
    reason: str
    paths: tuple[str, ...]
    exclude: tuple[str, ...] = ()
    docs: tuple[str, ...] | None = None      # None = de globale docs-lijst


@dataclass(frozen=True)
class Config:
    mode: str = DEFAULT_MODE
    docs: tuple[str, ...] = DEFAULT_DOCS
    ignore: tuple[str, ...] = DEFAULT_IGNORE
    rules: tuple[Rule, ...] = ()
    trailer: str = DEFAULT_TRAILER
    min_reason_len: int = DEFAULT_MIN_REASON_LEN
    git_timeout: int = DEFAULT_GIT_TIMEOUT
    max_report_files: int = DEFAULT_MAX_REPORT_FILES
    max_report_commits: int = DEFAULT_MAX_REPORT_COMMITS


@dataclass
class Commit:
    sha: str
    subject: str
    message: str
    files: list[str] = field(default_factory=list)
    exemption: str | None = None     # geldige reden uit de trailer


# --- config ---------------------------------------------------------------

def _str_list(value, where: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, str) or not isinstance(value, (list, tuple)):
        raise ConfigError(f"{where}: verwacht een lijst van patronen")
    out = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            raise ConfigError(f"{where}: patroon moet een niet-lege tekst zijn")
        out.append(item)
    return tuple(out)


def _positive_int(value, where: str, default: int) -> int:
    if value is None:
        return default
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ConfigError(f"{where}: verwacht een niet-negatief geheel getal")
    return value


def parse_config(data) -> Config:
    """Bouw een Config uit geladen YAML. Faalt hard op onbekende version."""
    if not isinstance(data, dict):
        raise ConfigError("bovenste niveau moet een mapping zijn")

    version = data.get("version")
    if version is None:
        raise ConfigError("version ontbreekt "
                          f"(ondersteund: {list(SUPPORTED_VERSIONS)})")
    if version not in SUPPORTED_VERSIONS:
        raise ConfigError(f"version {version!r} wordt niet ondersteund "
                          f"(ondersteund: {list(SUPPORTED_VERSIONS)})")

    mode = data.get("mode", DEFAULT_MODE)
    if mode not in MODES:
        raise ConfigError(f"mode {mode!r} onbekend (kies uit {list(MODES)})")

    docs = _str_list(data.get("docs"), "docs") or DEFAULT_DOCS
    ignore = _str_list(data.get("ignore"), "ignore") or DEFAULT_IGNORE

    raw_rules = data.get("rules") or []
    if not isinstance(raw_rules, list):
        raise ConfigError("rules: verwacht een lijst")
    rules = []
    for n, raw in enumerate(raw_rules, 1):
        if not isinstance(raw, dict):
            raise ConfigError(f"rules[{n}]: verwacht een mapping")
        name = raw.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ConfigError(f"rules[{n}]: name ontbreekt")
        paths = _str_list(raw.get("paths"), f"rules[{name}].paths")
        if not paths:
            raise ConfigError(f"rules[{name}]: paths mag niet leeg zijn")
        rule_docs = _str_list(raw.get("docs"), f"rules[{name}].docs")
        rules.append(Rule(
            name=name.strip(),
            reason=str(raw.get("reason") or "geen reden opgegeven in de config"),
            paths=paths,
            exclude=_str_list(raw.get("exclude"), f"rules[{name}].exclude"),
            docs=rule_docs or None,
        ))

    escape = data.get("escape") or {}
    if not isinstance(escape, dict):
        raise ConfigError("escape: verwacht een mapping")
    trailer = escape.get("trailer", DEFAULT_TRAILER)
    if not isinstance(trailer, str) or not trailer.strip():
        raise ConfigError("escape.trailer: verwacht een niet-lege tekst")

    report = data.get("report") or {}
    if not isinstance(report, dict):
        raise ConfigError("report: verwacht een mapping")

    return Config(
        mode=mode,
        docs=docs,
        ignore=ignore,
        rules=tuple(rules),
        trailer=trailer.strip(),
        min_reason_len=_positive_int(escape.get("min_reason_len"),
                                     "escape.min_reason_len",
                                     DEFAULT_MIN_REASON_LEN),
        git_timeout=_positive_int(data.get("git_timeout"), "git_timeout",
                                  DEFAULT_GIT_TIMEOUT),
        max_report_files=_positive_int(report.get("max_files"),
                                       "report.max_files",
                                       DEFAULT_MAX_REPORT_FILES),
        max_report_commits=_positive_int(report.get("max_commits"),
                                         "report.max_commits",
                                         DEFAULT_MAX_REPORT_COMMITS),
    )


def load_config(path: Path) -> Config | None:
    """None wanneer het bestand niet bestaat (= hook slaat zichzelf over)."""
    if not path.is_file():
        return None
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise ConfigError(f"onleesbare YAML: {exc}") from exc
    return parse_config(data)


# --- matching -------------------------------------------------------------

def compile_spec(patterns) -> pathspec.PathSpec:
    """Gitignore-globs (dus `**`, en een patroon zonder / matcht overal).

    GitWildMatchPattern is in pathspec 1.x deprecated maar bestaat in 0.12
    én 1.x; vandaar de versieband in de scriptheader. Wisselen naar de
    'gitignore'-factory kan pas als elke consumer op 1.x zit.
    """
    return pathspec.PathSpec.from_lines(
        pathspec.patterns.GitWildMatchPattern, list(patterns))


def matches(spec: pathspec.PathSpec, path: str) -> bool:
    return spec.match_file(path)


def required_paths(files, rule_spec, exclude_spec, ignore_spec) -> list[str]:
    """Paden die deze regel docs-plichtig maakt.

    Precedentie: ignore > exclude > paths.
    """
    hits = []
    for path in files:
        if matches(ignore_spec, path):
            continue
        if matches(exclude_spec, path):
            continue
        if matches(rule_spec, path):
            hits.append(path)
    return hits


def docs_paths(files, docs_spec) -> list[str]:
    """Gewijzigde docs. `ignore` telt hier bewust niet mee: die lijst zegt
    'deze wijziging vraagt geen docs', niet 'dit is geen docs'."""
    return [p for p in files if matches(docs_spec, p)]


# --- trailer --------------------------------------------------------------

def trailer_reason(message: str, trailer: str) -> str | None:
    """Laatste waarde van `<trailer>: ...` in het commitbericht, of None."""
    prefix = f"{trailer.lower()}:"
    found = None
    for line in message.splitlines():
        stripped = line.strip()
        if stripped.lower().startswith(prefix):
            found = stripped[len(prefix):].strip()
    return found


def valid_exemption(message: str, trailer: str, min_len: int) -> str | None:
    """Geldige vrijstelling, of None. Te korte reden telt niet."""
    reason = trailer_reason(message, trailer)
    if reason is None or len(reason) < min_len:
        return None
    return reason


# --- git ------------------------------------------------------------------

def git(repo: Path, args, timeout: int) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        capture_output=True, text=True, timeout=timeout,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    if result.returncode != 0:
        raise GitError(f"git {' '.join(args)}: "
                       f"{result.stderr.strip() or 'exit ' + str(result.returncode)}")
    return result.stdout


def zsplit(out: str) -> list[str]:
    return [part for part in out.split("\0") if part]


def rev_exists(repo: Path, ref: str, timeout: int) -> bool:
    try:
        git(repo, ["rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
            timeout)
    except GitError:
        return False
    return True


def changed_files(repo: Path, from_ref: str, to_ref: str,
                  timeout: int) -> list[str]:
    """Bestanden in de push. Drie punten, met terugval op twee punten als
    er geen merge-base is — dezelfde conventie als pre_commit/git.py."""
    base = ["diff", "--name-only", "--no-ext-diff", "-z"]
    try:
        return zsplit(git(repo, [*base, f"{from_ref}...{to_ref}"], timeout))
    except GitError:
        return zsplit(git(repo, [*base, f"{from_ref}..{to_ref}"], timeout))


def commits_in_range(repo: Path, from_ref: str, to_ref: str,
                     timeout: int) -> list[Commit]:
    """De commits die echt gepusht worden: twee punten, geen merges.

    Merges worden overgeslagen zodat hun inhoud niet dubbel telt; het
    werk zit al in de commits die eronder hangen.
    """
    out = git(repo, ["log", "--no-merges", "-z", "--format=%H%n%B",
                     f"{from_ref}..{to_ref}"], timeout)
    commits = []
    for entry in out.split("\0"):
        if not entry.strip():
            continue
        sha, _, message = entry.partition("\n")
        sha = sha.strip()
        commits.append(Commit(
            sha=sha,
            subject=message.strip().splitlines()[0] if message.strip() else "",
            message=message,
            files=zsplit(git(repo, ["diff-tree", "--no-commit-id",
                                    "--name-only", "--no-ext-diff", "-r",
                                    "-z", "--root", sha], timeout)),
        ))
    return commits


# --- refs -----------------------------------------------------------------

def resolve_refs(args, environ) -> tuple[str, str, str] | None:
    """(from_ref, to_ref, herkomst) of None. Raadt nooit een baseline."""
    if args.from_ref and args.to_ref:
        return args.from_ref, args.to_ref, "argumenten"
    for from_key, to_key in ENV_REF_PAIRS:
        from_ref, to_ref = environ.get(from_key), environ.get(to_key)
        if from_ref and to_ref:
            return from_ref, to_ref, f"{from_key}/{to_key}"
    return None


# --- gate -----------------------------------------------------------------

@dataclass
class Violation:
    rule: Rule
    paths: list[str]
    commits: list[Commit]


def evaluate(config: Config, files, commits) -> list[Violation]:
    """Welke regels zijn geschonden.

    Eisen komen van níét-vrijgestelde commits; of eraan voldaan is, wordt
    getoetst tegen de docs in de héle push (docs-as-code is een eis per
    PR, niet per losse commit).
    """
    ignore_spec = compile_spec(config.ignore)
    global_docs_spec = compile_spec(config.docs)
    violations = []
    for rule in config.rules:
        rule_spec = compile_spec(rule.paths)
        exclude_spec = compile_spec(rule.exclude)
        docs_spec = (compile_spec(rule.docs) if rule.docs
                     else global_docs_spec)

        demanding, hit_paths = [], []
        for commit in commits:
            if commit.exemption is not None:
                continue
            hits = required_paths(commit.files, rule_spec, exclude_spec,
                                  ignore_spec)
            if hits:
                demanding.append(commit)
                hit_paths.extend(hits)
        if not demanding:
            continue
        if docs_paths(files, docs_spec):
            continue
        violations.append(Violation(rule=rule,
                                    paths=sorted(set(hit_paths)),
                                    commits=demanding))
    return violations


def report(config: Config, from_ref: str, to_ref: str, source: str,
           files, commits, violations) -> None:
    exempt = [c for c in commits if c.exemption is not None]
    print(f"{PREFIX} diff {from_ref}..{to_ref} (via {source}); "
          f"{len(files)} bestand(en), {len(commits)} commit(s), "
          f"{len(exempt)} vrijgesteld, mode {config.mode}")
    for commit in exempt[:config.max_report_commits]:
        print(f"   vrijgesteld {commit.sha[:12]} ({config.trailer}: "
              f"{commit.exemption})")
    if not violations:
        print(f"{PREFIX} geen bevindingen")
        return
    for violation in violations:
        print(f"{PREFIX} regel '{violation.rule.name}' geschonden — "
              f"{violation.rule.reason}")
        shown = violation.paths[:config.max_report_files]
        for path in shown:
            print(f"   gewijzigd: {path}")
        if len(violation.paths) > len(shown):
            print(f"   ... en nog {len(violation.paths) - len(shown)} "
                  "bestand(en)")
        for commit in violation.commits[:config.max_report_commits]:
            print(f"   commit: {commit.sha[:12]} {commit.subject}")
        docs_expected = violation.rule.docs or config.docs
        print(f"   verwacht: een wijziging onder {list(docs_expected)}")
    print(f"{PREFIX} vrijstellen kan per commit met de trailer "
          f"'{config.trailer}: <reden van minstens "
          f"{config.min_reason_len} tekens>'")
    print(f"{PREFIX} lijkt de diff te breed? Controleer de refs hierboven; "
          "een verouderde remote-tracking ref na `git fetch` is de "
          "gebruikelijke oorzaak.")


# --- main -----------------------------------------------------------------

def main(argv=None, environ=None) -> int:
    parser = argparse.ArgumentParser(
        description="Gate: docs wijzigen mee met de code (docs-as-code).")
    parser.add_argument("--repo", default=".", help="repo-root (default .)")
    parser.add_argument("--config", default=None,
                        help=f"pad naar de config (default <repo>/{CONFIG_NAME})")
    parser.add_argument("--from-ref", default=None)
    parser.add_argument("--to-ref", default=None)
    parser.add_argument("--mode", choices=MODES, default=None,
                        help="overschrijft mode uit de config")
    args = parser.parse_args(argv)
    environ = os.environ if environ is None else environ

    repo = Path(args.repo).resolve()
    if not repo.is_dir():
        print(f"fout: geen directory: {args.repo}", file=sys.stderr)
        return 2

    config_path = Path(args.config) if args.config else repo / CONFIG_NAME
    try:
        config = load_config(config_path)
    except ConfigError as exc:
        print(f"{PREFIX} FOUT in {config_path}: {exc}", file=sys.stderr)
        return 2
    if config is None:
        print(f"{PREFIX} overgeslagen — geen {config_path.name} in {repo}")
        return 0
    if args.mode:
        config = replace(config, mode=args.mode)

    refs = resolve_refs(args, environ)
    if refs is None:
        print(f"{PREFIX} overgeslagen — geen diff-context "
              "(--from-ref/--to-ref of PRE_COMMIT_FROM_REF/TO_REF)")
        return 0
    from_ref, to_ref, source = refs

    for label, ref in (("from-ref", from_ref), ("to-ref", to_ref)):
        if not rev_exists(repo, ref, config.git_timeout):
            print(f"{PREFIX} kon diff niet bepalen — {label} {ref!r} bestaat "
                  "niet in deze repo (force-push of opgeruimd object?)")
            return 0
    try:
        files = changed_files(repo, from_ref, to_ref, config.git_timeout)
        commits = commits_in_range(repo, from_ref, to_ref, config.git_timeout)
    except (GitError, subprocess.TimeoutExpired) as exc:
        print(f"{PREFIX} kon diff niet bepalen — {exc}")
        return 0

    for commit in commits:
        commit.exemption = valid_exemption(commit.message, config.trailer,
                                           config.min_reason_len)

    violations = evaluate(config, files, commits)
    report(config, from_ref, to_ref, source, files, commits, violations)
    if violations and config.mode == "enforce":
        return 1
    if violations:
        print(f"{PREFIX} mode warn — niet geblokkeerd")
    return 0


if __name__ == "__main__":
    sys.exit(main())
