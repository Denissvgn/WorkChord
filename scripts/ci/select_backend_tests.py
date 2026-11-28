#!/usr/bin/env python3
"""Select the backend test files a pull request change can affect (shadow mode).

The selector compares ``BASE_SHA`` and ``HEAD_SHA`` (environment, or
``--base``/``--head``), reads the changed paths from Git and prints one JSON
object::

    {"mode": "selected" | "full", "reasons": [...], "tests": [...],
     "smoke": [...], "sources": {...}}

``tests`` are pytest paths under ``backend/tests`` and already include the
always-run set (``smoke``). ``mode: "full"`` means the caller must run the
whole backend suite; ``tests`` is then empty. The script never fails a build:
any doubt or error produces ``full``.

The graph is read from the working tree, so the checkout must be at
``HEAD_SHA``; otherwise the result is ``full``.

Selection, in order:

1. Shared ground selects the full suite: any conftest, test support helpers,
   migrations, models, configuration, database runtime, authority, commands,
   the agent skill sources and their build script, lockfiles,
   ``pyproject.toml``, ``.github`` and this script.
2. A deleted or renamed Python file, or a non-Python file under
   ``backend/app`` or ``backend/tests``, selects the full suite.
3. Changed or added backend test files are selected directly.
4. Every changed path is traced, transitively, through a static graph of the
   Python files under ``backend/app``, ``backend/tests`` and ``scripts``
   built with Python's ``ast`` module. A file depends on another when it

   * imports it (absolute, relative, or a bare name put on ``sys.path``),
   * is a test file below a ``conftest.py`` or package ``__init__.py`` in
     ``backend/tests`` (pytest loads those for every test under their
     directory), or
   * mentions it in its source: its repository path or a path suffix of at
     least two components, its file name (with the parent directory name
     when the file name is not unique in the repository) or its dotted
     module name. This covers ``runpy.run_path``, ``importlib`` loading by
     path, ``subprocess`` and ``python -m`` calls. A non-Python path also
     matches files that mention one of its directories (two or more
     components).

   Test files reached this way are selected.
5. The always-run set is added. When the result covers every backend test,
   the mode is ``full``.

``--engine wiki`` also queries the llm-wiki knowledge graph (``impact`` on the
changed backend modules, then incoming ``imports`` edges from the committed
snapshot) and unions it with the static selection. It falls back to ``full``
when the wiki snapshot revision is not an ancestor of (or equal to) the base,
when llm-wiki is not importable, or when a result is truncated, ambiguous,
unresolved, not ``ready`` or reports ``found: false`` for a changed module.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
from typing import Any, Callable, Iterable

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
WIKI_DIR = PurePosixPath("docs/llm_wiki")
TEST_ROOT = PurePosixPath("backend/tests")
ZERO_SHA = "0" * 40

# Always run. Each guards a boundary that many unrelated changes can break
# without importing the module under test:
SMOKE_TESTS: tuple[str, ...] = (
    # authority: caller identity, scopes and managed-mode refusals
    "backend/tests/test_managed_authority.py",
    "backend/tests/test_strict_caller_matrix.py",
    "backend/tests/test_authority_migrations.py",
    # migrations: the schema chain upgrades cleanly on both engines
    "backend/tests/migrations/test_initial_schema.py",
    "backend/tests/migrations/test_sqlite_migrations.py",
    "backend/tests/migrations/test_postgresql_migrations.py",
    # runtime boundaries: process roles, query limits, advertised features
    "backend/tests/test_runtime_boundaries.py",
    "backend/tests/test_process_roles.py",
    "backend/tests/database/test_runtime_policy.py",
    "backend/tests/test_server_features.py",
    # generated contracts: the client and mobile contracts are exported from
    # the whole application (every router and schema), so any API change can
    # alter them. Two files are far cheaper than the full suite that a rule
    # on backend/app/routers or backend/app/schemas would trigger.
    "backend/tests/test_client_contract.py",
    "backend/tests/test_mobile_contract.py",
    # source scanners: these read every Python file under backend/app (or the
    # repository) instead of importing what they check
    "backend/tests/database/test_deployment_topology.py",
    "backend/tests/test_refusal_next_steps.py",
)

SHARED_PREFIXES: tuple[str, ...] = (
    ".github/",
    "agent-skills/",
    "backend/app/migrations/",
    "backend/app/models/",
    "backend/app/config/",
    "backend/app/database_migration/",
    "backend/tests/support/",
)
SHARED_FILES: frozenset[str] = frozenset(
    {
        "backend/app/config.py",
        "backend/app/authority.py",
        "backend/app/http_authority.py",
        "backend/app/commands.py",
        "backend/pyproject.toml",
        "backend/uv.lock",
        "pyproject.toml",
        "scripts/build_agent_skills.py",
        "scripts/ci/select_backend_tests.py",
    }
)
SHARED_NAMES: frozenset[str] = frozenset({"conftest.py", "pyproject.toml", "uv.lock"})

# Python roots on the test path: backend/ (``app``, ``tests``) and the
# repository root (``scripts``).
PYTHON_ROOTS: tuple[tuple[str, str], ...] = (
    ("backend/app", "app"),
    ("backend/tests", "tests"),
    ("scripts", "scripts"),
)
ROOT_PACKAGES = frozenset(package for _, package in PYTHON_ROOTS)

# File names that say nothing about which file is meant.
GENERIC_NAMES = frozenset({"__init__.py", "__main__.py", "conftest.py"})

# Path-like or dotted words in source text: quoted paths, dotted modules.
_TOKEN = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_.\-/]*")


class FullSuite(Exception):
    """Raised when the selection must fall back to the full suite."""


# --------------------------------------------------------------------------- git


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, check=False
    )


def _rev_parse(root: Path, revision: str) -> str:
    result = _git(root, "rev-parse", "--verify", "--quiet", f"{revision}^{{commit}}")
    return result.stdout.strip() if result.returncode == 0 else ""


def require_checkout_at(root: Path, head: str) -> None:
    """The graph is read from the working tree; it must be the head commit."""
    expected = _rev_parse(root, head)
    actual = _rev_parse(root, "HEAD")
    if not expected or expected != actual:
        raise FullSuite(
            f"checkout is at {actual[:12] or 'unknown'}, not the head commit {head[:12]}"
        )


def changed_paths(root: Path, base: str, head: str) -> dict[str, str]:
    """Return ``{path: status}`` for the change from the merge base to head."""
    if not base or not head or base == ZERO_SHA:
        raise FullSuite("missing base or head commit")
    result = _git(root, "diff", "--name-status", "--no-renames", "-z", f"{base}...{head}")
    if result.returncode != 0:
        raise FullSuite(f"git diff failed: {result.stderr.strip()[:200]}")
    fields = result.stdout.split("\0")
    paths: dict[str, str] = {}
    index = 0
    while index + 1 < len(fields):
        status = fields[index]
        if not status:
            break
        # Renames and copies are disabled above, so each entry has one path.
        paths[fields[index + 1]] = status[:1]
        index += 2
    if not paths:
        raise FullSuite("empty change")
    return paths


def tracked_files(root: Path) -> list[str]:
    result = _git(root, "ls-files", "-z")
    if result.returncode != 0:
        raise FullSuite(f"git ls-files failed: {result.stderr.strip()[:200]}")
    return sorted(path for path in result.stdout.split("\0") if path)


def is_ancestor(root: Path, ancestor: str, descendant: str) -> bool:
    return _git(root, "merge-base", "--is-ancestor", ancestor, descendant).returncode == 0


# ------------------------------------------------------------------ path rules


def is_shared_ground(path: str) -> bool:
    """Return True when a change to ``path`` can affect any backend test."""
    pure = PurePosixPath(path)
    if path in SHARED_FILES or pure.name in SHARED_NAMES:
        return True
    if any(path.startswith(prefix) for prefix in SHARED_PREFIXES):
        return True
    if pure.name.endswith(".lock") and path.startswith("backend/"):
        return True
    if path.startswith("backend/app/") and pure.name.startswith("database"):
        return True
    return False


def is_test_file(path: str) -> bool:
    pure = PurePosixPath(path)
    return (
        path.startswith(f"{TEST_ROOT}/")
        and pure.suffix == ".py"
        and pure.name.startswith("test_")
    )


def module_name(path: str) -> str | None:
    """Map a repository path to its importable module name, or None."""
    pure = PurePosixPath(path)
    if pure.suffix != ".py":
        return None
    for prefix, package in PYTHON_ROOTS:
        if path == f"{prefix}/__init__.py":
            return package
        if path.startswith(f"{prefix}/"):
            relative = PurePosixPath(path[len(prefix) + 1 :]).with_suffix("")
            parts = [package, *relative.parts]
            if parts[-1] == "__init__":
                parts.pop()
            return ".".join(parts)
    return None


# ---------------------------------------------------------------- static graph


def _imported_names(tree: ast.AST, own_module: str, is_package: bool) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                anchor = own_module.split(".")
                if not is_package:
                    anchor = anchor[:-1]
                if node.level > 1:
                    anchor = anchor[: len(anchor) - (node.level - 1)]
                base = ".".join([*anchor, *([node.module] if node.module else [])])
            else:
                base = node.module or ""
            if base:
                names.add(base)
                names.update(f"{base}.{alias.name}" for alias in node.names)
    return names


def _tokens(text: str) -> set[str]:
    """Return the path and dotted-name words of ``text`` and their parts.

    ``"scripts/ci/x.py"`` yields every contiguous run of its components
    (``scripts/ci``, ``ci/x.py``, ``x.py`` ...); ``app.cli.closeout`` yields
    its dotted prefixes.
    """
    found: set[str] = set()
    for raw in set(_TOKEN.findall(text)):
        token = raw.rstrip("./-")
        if not token:
            continue
        found.add(token)
        if "/" in token:
            parts = [part for part in token.split("/") if part]
            for start in range(len(parts)):
                for end in range(start + 1, len(parts) + 1):
                    found.add("/".join(parts[start:end]))
        elif "." in token:
            parts = token.split(".")
            for end in range(1, len(parts)):
                found.add(".".join(parts[:end]))
    return found


class Repository:
    """The Python files of the head checkout and how they depend on each other."""

    def __init__(self, root: Path, files: Iterable[str] | None = None) -> None:
        self.root = root
        tracked = list(files) if files is not None else tracked_files(root)
        self.python = sorted(path for path in tracked if module_name(path))
        self.tests = {path for path in self.python if is_test_file(path)}
        self.by_module = {module_name(path): path for path in self.python}
        name_counts: dict[str, int] = {}
        for path in tracked:
            name = PurePosixPath(path).name
            name_counts[name] = name_counts.get(name, 0) + 1
        self.unique_names = {name for name, count in name_counts.items() if count == 1}
        # Dotted suffixes, for bare imports of a directory put on sys.path
        # (``import android_qualification`` for scripts/ci/...).
        self.by_suffix: dict[str, set[str]] = {}
        for module, path in self.by_module.items():
            parts = module.split(".")
            for start in range(1, len(parts)):
                self.by_suffix.setdefault(".".join(parts[start:]), set()).add(path)

        self.imports: dict[str, set[str]] = {}
        self.token_index: dict[str, set[str]] = {}
        for path in self.python:
            try:
                text = (root / path).read_text(encoding="utf-8")
                tree = ast.parse(text, filename=path)
            except (OSError, SyntaxError, UnicodeDecodeError, ValueError) as exc:
                raise FullSuite(f"cannot parse {path}: {exc.__class__.__name__}") from exc
            self.imports[path] = self._resolve(tree, path)
            for token in _tokens(text):
                self.token_index.setdefault(token, set()).add(path)

        self.importers: dict[str, set[str]] = {}
        for importer, targets in self.imports.items():
            for target in targets:
                self.importers.setdefault(target, set()).add(importer)
        # pytest loads every conftest.py and package __init__.py above a
        # test module before the module itself.
        for implicit in self.python:
            if implicit.startswith(f"{TEST_ROOT}/") and PurePosixPath(implicit).name in (
                "conftest.py",
                "__init__.py",
            ):
                directory = f"{PurePosixPath(implicit).parent}/"
                self.importers.setdefault(implicit, set()).update(
                    test for test in self.tests if test.startswith(directory)
                )
        self._mentions: dict[str, set[str]] = {}

    def _resolve(self, tree: ast.AST, path: str) -> set[str]:
        own = module_name(path) or ""
        targets: set[str] = set()
        for name in _imported_names(tree, own, path.endswith("__init__.py")):
            parts = name.split(".")
            top = parts[0]
            # Importing a.b.c also executes a and a.b: record every module on
            # the way that exists.
            for length in range(len(parts), 0, -1):
                prefix = ".".join(parts[:length])
                target = self.by_module.get(prefix)
                if target:
                    targets.add(target)
                elif top not in ROOT_PACKAGES and top not in sys.stdlib_module_names:
                    targets.update(self.by_suffix.get(prefix, ()))
        targets.discard(path)
        return targets

    def needles(self, path: str) -> list[tuple[str, ...]]:
        """Return word groups; a file mentions ``path`` when it has all of a group."""
        pure = PurePosixPath(path)
        parts = pure.parts
        groups: list[tuple[str, ...]] = [
            ("/".join(parts[start:]),) for start in range(len(parts) - 1)
        ]
        if pure.name not in GENERIC_NAMES:
            if pure.name in self.unique_names:
                groups.append((pure.name,))
            elif len(parts) >= 2:
                groups.append((pure.name, parts[-2]))
        module = module_name(path)
        if module and "." in module:
            groups.append((module,))
        if not module:
            groups.extend(("/".join(parts[:end]),) for end in range(2, len(parts)))
        return groups

    def mentioning(self, path: str) -> set[str]:
        """Return the Python files whose source mentions ``path``."""
        cached = self._mentions.get(path)
        if cached is not None:
            return cached
        found: set[str] = set()
        for group in self.needles(path):
            sets = [self.token_index.get(token, set()) for token in group]
            found |= set.intersection(*sets) if sets else set()
        found.discard(path)
        self._mentions[path] = found
        return found

    def dependents(self, path: str) -> set[str]:
        return self.importers.get(path, set()) | self.mentioning(path)

    def affected(self, paths: Iterable[str]) -> set[str]:
        """Return every Python file that depends, transitively, on a path."""
        start: set[str] = set()
        for path in paths:
            if path in self.imports:
                start.add(path)
            start |= self.mentioning(path)
        return start | reverse_closure(start, self.dependents)


def reverse_closure(start: Iterable[str], incoming: Callable[[str], Iterable[str]]) -> set[str]:
    """Return every path that reaches a start path through incoming edges."""
    seen: set[str] = set()
    stack = list(start)
    while stack:
        current = stack.pop()
        for importer in incoming(current):
            if importer not in seen:
                seen.add(importer)
                stack.append(importer)
    return seen


# ------------------------------------------------------------------ wiki graph


def wiki_revision(root: Path) -> str:
    """Return the commit the wiki knowledge snapshot was evaluated at."""
    record = json.loads((root / WIKI_DIR / ".llm-wiki-knowledge.json").read_text(encoding="utf-8"))
    found: set[str] = set()
    stack: list[Any] = [record]
    while stack:
        value = stack.pop()
        if isinstance(value, dict):
            revision = value.get("evaluated_revision")
            if isinstance(revision, str):
                found.add(revision)
            stack.extend(value.values())
        elif isinstance(value, list):
            stack.extend(value)
    if len(found) != 1:
        raise FullSuite(f"wiki snapshot has {len(found)} evaluated revisions")
    revision = found.pop()
    if not revision.startswith("git:"):
        raise FullSuite("wiki snapshot revision is not a Git commit")
    return revision[4:]


def _require_clean(payload: dict[str, Any], what: str) -> None:
    if payload.get("truncated"):
        raise FullSuite(f"{what} result truncated")
    for name, bound in (payload.get("bounds") or {}).items():
        if isinstance(bound, dict) and bound.get("truncated"):
            raise FullSuite(f"{what} result bounded ({name})")
    if payload.get("ambiguous"):
        raise FullSuite(f"{what} result ambiguous")
    knowledge = payload.get("knowledge") or {}
    if knowledge and knowledge.get("availability") != "ready":
        raise FullSuite(f"{what} knowledge {knowledge.get('availability')}")


class WikiGraph:
    """Read-only llm-wiki queries; never syncs or writes the wiki."""

    def __init__(self, root: Path) -> None:
        try:
            from llm_wiki_cli import api  # type: ignore[import-not-found]
        except Exception as exc:  # noqa: BLE001 - any import problem means unavailable
            raise FullSuite(f"llm-wiki unavailable: {exc.__class__.__name__}") from exc
        self.api = api
        self.root = root
        self._service = None

    def impact_each(self, paths: list[str]) -> Iterable[tuple[str, dict[str, Any]]]:
        """Run one impact query per path, in parallel processes."""
        from concurrent.futures import ProcessPoolExecutor

        workers = max(1, min(len(paths), os.cpu_count() or 1, 4))
        with ProcessPoolExecutor(max_workers=workers) as pool:
            results = pool.map(_impact_one, [(str(self.root), path) for path in paths])
            yield from zip(paths, results)

    def incoming_imports(self, locator: str) -> dict[str, Any]:
        if self._service is None:
            self._service = self.api.build_snapshot_documentation_query_service(
                wiki_root=(self.root / WIKI_DIR).resolve(), limit=1000
            )
        # A result over the public size ceiling comes back truncated, which
        # selects the full suite.
        return self.api.traverse_typed_graph(
            locator,
            direction="incoming",
            kinds=["imports"],
            include_evidence=False,
            service=self._service,
            limit=1000,
        )


def _impact_one(arguments: tuple[str, str]) -> dict[str, Any]:
    from llm_wiki_cli import api  # type: ignore[import-not-found]

    root, path = arguments
    return api.query_documentation(
        {"operation": "impact", "paths": [path], "limit": 100},
        src_dir=root,
        wiki_dir=str(Path(root) / WIKI_DIR),
    )


def wiki_selection(
    root: Path, base: str, modules: list[str], graph: WikiGraph | None = None
) -> set[str]:
    revision = wiki_revision(root)
    if not is_ancestor(root, revision, base):
        raise FullSuite(f"wiki snapshot {revision[:12]} is not an ancestor of the base")
    graph = graph or WikiGraph(root)
    # One impact query per path: a combined result for a few large modules
    # exceeds the result ceiling and comes back empty and truncated.
    locators: dict[str, str] = {}
    for path, impact in graph.impact_each(modules):
        _require_clean(impact, f"impact of {path}")
        if not impact.get("found"):
            raise FullSuite(f"impact found: false for {path}")
        for concept in impact.get("concepts", []):
            if concept.get("concept_kind") == "source-module" and concept.get("source_path"):
                locators[concept["source_path"]] = concept["locator"]
    missing = [path for path in modules if path not in locators]
    if missing:
        raise FullSuite(f"impact found no module concept for {missing[0]}")

    path_to_locator: dict[str, str] = dict(locators)
    importers_cache: dict[str, set[str]] = {}

    def incoming(path: str) -> set[str]:
        locator = path_to_locator.get(path)
        if locator is None:
            return set()
        if locator in importers_cache:
            return importers_cache[locator]
        payload = graph.incoming_imports(locator)
        _require_clean(payload, f"imports of {path}")
        if not payload.get("found"):
            raise FullSuite(f"typed graph found: false for {path}")
        importers: set[str] = set()
        for edge in payload.get("edges", []):
            if edge.get("resolution") != "resolved":
                raise FullSuite(f"{edge.get('resolution')} import edge for {path}")
            related = edge.get("related_concept") or {}
            source = related.get("source_path")
            if not source:
                raise FullSuite(f"import edge without a source for {path}")
            if related.get("locator"):
                path_to_locator.setdefault(source, related["locator"])
            importers.add(source)
        importers_cache[locator] = importers
        return importers

    affected = reverse_closure(modules, incoming)
    return {path for path in affected if is_test_file(path)}


# ------------------------------------------------------------------- selection


def selection_for(repository: Repository, changes: dict[str, str]) -> tuple[set[str], dict[str, list[str]]]:
    """Return the tests a change selects (always-run set excluded) and why.

    Raises ``FullSuite`` when the change needs the whole suite.
    """
    shared = sorted(path for path in changes if is_shared_ground(path))
    if shared:
        raise FullSuite(f"shared ground changed: {', '.join(shared[:5])}")
    removed = sorted(
        path for path, status in changes.items() if status in "DRC" and path.endswith(".py")
    )
    if removed:
        raise FullSuite(f"Python file deleted or renamed: {removed[0]}")
    for prefix, what in ((f"{TEST_ROOT}/", "test data"), ("backend/app/", "application data")):
        data = sorted(
            path for path in changes if path.startswith(prefix) and not path.endswith(".py")
        )
        if data:
            raise FullSuite(f"{what} changed: {data[0]}")

    present = [path for path, status in changes.items() if status != "D"]
    direct = {path for path in present if is_test_file(path)}
    python = [path for path in present if module_name(path)]
    other = [path for path in present if not module_name(path)]
    graph = {path for path in repository.affected(python) if is_test_file(path)}
    referenced = {path for path in repository.affected(other) if is_test_file(path)}
    sources = {
        "changed_tests": sorted(direct),
        "ast": sorted(graph),
        "references": sorted(referenced),
    }
    return direct | graph | referenced, sources


def select(
    root: Path,
    base: str,
    head: str,
    *,
    engine: str = "ast",
    wiki_graph: WikiGraph | None = None,
) -> dict[str, Any]:
    reasons: list[str] = []
    sources: dict[str, list[str]] = {}
    smoke = [path for path in SMOKE_TESTS if (root / path).exists()]
    try:
        changes = changed_paths(root, base, head)
        require_checkout_at(root, head)
        repository = Repository(root)
        selected, sources = selection_for(repository, changes)

        backend_modules = sorted(
            path
            for path, status in changes.items()
            if status != "D" and path.startswith("backend/") and module_name(path)
            and not is_test_file(path)
        )
        if engine == "wiki" and backend_modules:
            wiki = wiki_selection(root, base, backend_modules, wiki_graph)
            sources["wiki"] = sorted(wiki)
            selected |= wiki
        elif engine == "wiki":
            reasons.append("no changed backend modules; llm-wiki not consulted")
        reasons.append(
            f"{len(changes)} changed paths, {len(sources['changed_tests'])} changed tests"
        )
        tests = sorted((selected & repository.tests) | set(smoke))
        if set(tests) >= repository.tests:
            raise FullSuite("selection covers every backend test")
        return {
            "mode": "selected",
            "reasons": reasons,
            "tests": tests,
            "smoke": smoke,
            "sources": sources,
        }
    except FullSuite as exc:
        reasons.append(str(exc))
    except Exception as exc:  # noqa: BLE001 - fail toward the full suite
        reasons.append(f"selector error: {exc.__class__.__name__}: {str(exc)[:200]}")
    return {"mode": "full", "reasons": reasons, "tests": [], "smoke": smoke, "sources": sources}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", default=os.environ.get("BASE_SHA", ""))
    parser.add_argument("--head", default=os.environ.get("HEAD_SHA", ""))
    parser.add_argument("--root", type=Path, default=REPOSITORY_ROOT)
    parser.add_argument(
        "--engine",
        choices=("ast", "wiki"),
        default="ast",
        help="ast: static graph only (default); wiki: static graph unioned with llm-wiki",
    )
    args = parser.parse_args(argv)
    print(json.dumps(select(args.root, args.base, args.head, engine=args.engine), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
