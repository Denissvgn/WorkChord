#!/usr/bin/env python3
"""Select the backend test files a pull request change can affect (shadow mode).

The selector compares ``BASE_SHA`` and ``HEAD_SHA`` (environment, or
``--base``/``--head``), reads the changed paths from Git and prints one JSON
object::

    {"mode": "selected" | "full", "reasons": [...], "tests": [...],
     "smoke": [...], "sources": {...}}

``tests`` are pytest paths under ``backend/tests`` and already include the
``smoke`` set. ``mode: "full"`` means the caller must run the whole backend
suite; ``tests`` is then empty. The script never fails a build: any doubt or
error produces ``full``.

Selection, in order:

1. Shared ground (any conftest, migrations, models, configuration, database
   runtime, authority, commands, lockfiles, ``pyproject.toml``, ``.github`` and
   this script) selects the full suite.
2. Changed or added backend test files are selected directly.
3. Changed Python modules are traced through reverse imports, transitively, to
   the test files that import them. Two graphs are used and unioned: the
   llm-wiki knowledge graph (``impact`` on the changed paths, then incoming
   ``imports`` edges from the committed snapshot) and a static graph built from
   the head checkout with Python's ``ast`` module.
4. Changed non-Python files select the test files whose source mentions the
   file name or its leading directories.
5. The smoke set is always added.

The wiki path falls back to ``full`` when the wiki snapshot revision is not an
ancestor of (or equal to) the base, when llm-wiki is not importable, or when
an impact or traversal result is truncated, ambiguous, unresolved, not
``ready`` or reports ``found: false`` for a changed module.

``--engine ast`` skips llm-wiki and uses only the static graph; it exists to
compare the two selectors.
"""

from __future__ import annotations

import argparse
import ast
import json
import os
from pathlib import Path, PurePosixPath
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
)

SHARED_PREFIXES: tuple[str, ...] = (
    ".github/",
    "backend/app/migrations/",
    "backend/app/models/",
    "backend/app/config/",
    "backend/app/database_migration/",
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


class FullSuite(Exception):
    """Raised when the selection must fall back to the full suite."""


# --------------------------------------------------------------------------- git


def _git(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True, check=False
    )


def changed_paths(root: Path, base: str, head: str) -> dict[str, str]:
    """Return ``{path: status}`` for the change from the merge base to head."""
    if not base or not head or base == ZERO_SHA:
        raise FullSuite("missing base or head commit")
    result = _git(root, "diff", "--name-status", "--no-renames", f"{base}...{head}")
    if result.returncode != 0:
        raise FullSuite(f"git diff failed: {result.stderr.strip()[:200]}")
    paths: dict[str, str] = {}
    for line in result.stdout.splitlines():
        status, _, path = line.partition("\t")
        if path:
            paths[path] = status[:1]
    if not paths:
        raise FullSuite("empty change")
    return paths


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


def python_files(root: Path) -> list[str]:
    files: list[str] = []
    for prefix, _ in PYTHON_ROOTS:
        base = root / prefix
        if base.is_dir():
            files.extend(
                path.relative_to(root).as_posix()
                for path in base.rglob("*.py")
                if "node_modules" not in path.parts
            )
    return sorted(files)


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
                anchor = anchor[: len(anchor) - (node.level - 1)] if node.level > 1 else anchor
                base = ".".join([*anchor, *([node.module] if node.module else [])])
            else:
                base = node.module or ""
            if base:
                names.add(base)
                names.update(f"{base}.{alias.name}" for alias in node.names)
    return names


def static_import_graph(root: Path, files: Iterable[str]) -> dict[str, set[str]]:
    """Return ``{importer path: imported paths}`` for the given Python files."""
    by_module = {name: path for path in files if (name := module_name(path))}
    graph: dict[str, set[str]] = {}
    for path in by_module.values():
        try:
            tree = ast.parse((root / path).read_text(encoding="utf-8"), filename=path)
        except (OSError, SyntaxError, UnicodeDecodeError) as exc:
            raise FullSuite(f"cannot parse {path}: {exc.__class__.__name__}") from exc
        own = module_name(path) or ""
        targets: set[str] = set()
        for name in _imported_names(tree, own, path.endswith("__init__.py")):
            # Importing a.b.c also executes a and a.b; only record the deepest
            # module that exists, plus the packages on the way.
            parts = name.split(".")
            for length in range(len(parts), 0, -1):
                target = by_module.get(".".join(parts[:length]))
                if target:
                    targets.add(target)
        targets.discard(path)
        graph[path] = targets
    return graph


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


def static_selection(root: Path, modules: Iterable[str]) -> set[str]:
    graph = static_import_graph(root, python_files(root))
    reverse: dict[str, set[str]] = {}
    for importer, targets in graph.items():
        for target in targets:
            reverse.setdefault(target, set()).add(importer)
    affected = reverse_closure(modules, lambda path: reverse.get(path, ()))
    return {path for path in affected if is_test_file(path)}


def reference_selection(root: Path, paths: Iterable[str]) -> set[str]:
    """Select test files whose text names a changed non-Python file."""
    needles: set[str] = set()
    for path in paths:
        pure = PurePosixPath(path)
        if len(pure.name) >= 6:
            needles.add(pure.name)
        if len(pure.parts) >= 3:
            needles.add("/".join(pure.parts[:2]))
    if not needles:
        return set()
    selected: set[str] = set()
    for test in (root / TEST_ROOT).rglob("test_*.py"):
        text = test.read_text(encoding="utf-8", errors="replace")
        if any(needle in text for needle in needles):
            selected.add(test.relative_to(root).as_posix())
    return selected


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
        traverse = type(self._service).traverse_typed_graph
        # The public result is capped at 64 KiB (about ten edges); the
        # undecorated traversal applies the same filters and the row limit
        # without that byte ceiling.
        traverse = getattr(traverse, "__wrapped__", traverse)
        return traverse(
            self._service,
            locator,
            direction="incoming",
            kinds=["imports"],
            origins=None,
            resolutions=None,
            include_evidence=False,
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
    # exceeds the 64 KiB result ceiling and comes back empty and truncated.
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
    locator_to_path = {locator: path for path, locator in locators.items()}
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
                locator_to_path.setdefault(related["locator"], source)
            importers.add(source)
        importers_cache[locator] = importers
        return importers

    affected = reverse_closure(modules, incoming)
    return {path for path in affected if is_test_file(path)}


# ------------------------------------------------------------------- selection


def select(
    root: Path,
    base: str,
    head: str,
    *,
    engine: str = "wiki",
    wiki_graph: WikiGraph | None = None,
) -> dict[str, Any]:
    reasons: list[str] = []
    sources: dict[str, list[str]] = {}
    try:
        changes = changed_paths(root, base, head)
        shared = sorted(path for path in changes if is_shared_ground(path))
        if shared:
            raise FullSuite(f"shared ground changed: {', '.join(shared[:5])}")
        tests_dir_other = sorted(
            path
            for path in changes
            if path.startswith(f"{TEST_ROOT}/")
            and not is_test_file(path)
            and PurePosixPath(path).suffix != ".py"
        )
        if tests_dir_other:
            raise FullSuite(f"test data changed: {tests_dir_other[0]}")

        present = {path for path, status in changes.items() if status != "D"}
        direct = {path for path in present if is_test_file(path)}
        sources["changed_tests"] = sorted(direct)
        modules = sorted(
            path
            for path in changes
            if module_name(path) and not is_test_file(path) and path not in direct
        )
        other = sorted(path for path in changes if not module_name(path))

        static = static_selection(root, modules) if modules else set()
        sources["ast"] = sorted(static)
        referenced = reference_selection(root, other) if other else set()
        sources["references"] = sorted(referenced)
        selected = direct | static | referenced

        backend_modules = [path for path in modules if path.startswith("backend/")]
        if engine == "wiki" and backend_modules:
            wiki = wiki_selection(root, base, backend_modules, wiki_graph)
            sources["wiki"] = sorted(wiki)
            selected |= wiki
        elif engine == "wiki":
            reasons.append("no changed backend modules; llm-wiki not consulted")
        reasons.append(
            f"{len(changes)} changed paths, {len(modules)} Python modules, "
            f"{len(direct)} changed tests"
        )
        smoke = [path for path in SMOKE_TESTS if (root / path).exists()]
        tests = sorted((selected & existing_tests(root)) | set(smoke))
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
    return {"mode": "full", "reasons": reasons, "tests": [], "smoke": list(SMOKE_TESTS), "sources": sources}


def existing_tests(root: Path) -> set[str]:
    return {path.relative_to(root).as_posix() for path in (root / TEST_ROOT).rglob("test_*.py")}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", default=os.environ.get("BASE_SHA", ""))
    parser.add_argument("--head", default=os.environ.get("HEAD_SHA", ""))
    parser.add_argument("--root", type=Path, default=REPOSITORY_ROOT)
    parser.add_argument("--engine", choices=("wiki", "ast"), default="wiki")
    args = parser.parse_args(argv)
    print(json.dumps(select(args.root, args.base, args.head, engine=args.engine), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
