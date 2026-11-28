# select_backend_tests Module

**Path:** `scripts/ci/select_backend_tests.py`

## Description

Select the backend test files a pull request change can affect (shadow mode).

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

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `argparse` | `argparse` |
| `ast` | `ast` |
| `concurrent.futures` | `ProcessPoolExecutor` |
| `json` | `json` |
| `llm_wiki_cli` | `api`, `api` |
| `os` | `os` |
| `pathlib` | `Path`, `PurePosixPath` |
| `subprocess` | `subprocess` |
| `sys` | `sys` |
| `typing` | `Any`, `Callable`, `Iterable` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 1 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [FullSuite](../entities/FullSuite.md) | 104 | `Exception` | Raised when the selection must fall back to the full suite. |
| [WikiGraph](../entities/WikiGraph.md) | 321 | — | Read-only llm-wiki queries; never syncs or writes the wiki. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_git` | `(root: Path, *args: str) -> subprocess.CompletedProcess[str]` | — | — |
| `changed_paths` | `(root: Path, base: str, head: str) -> dict[str, str]` | — | Return ``{path: status}`` for the change from the merge base to head. |
| `is_ancestor` | `(root: Path, ancestor: str, descendant: str) -> bool` | — | — |
| `is_shared_ground` | `(path: str) -> bool` | — | Return True when a change to ``path`` can affect any backend test. |
| `is_test_file` | `(path: str) -> bool` | — | — |
| `module_name` | `(path: str) -> str \| None` | — | Map a repository path to its importable module name, or None. |
| `python_files` | `(root: Path) -> list[str]` | — | — |
| `_imported_names` | `(tree: ast.AST, own_module: str, is_package: bool) -> set[str]` | — | — |
| `static_import_graph` | `(root: Path, files: Iterable[str]) -> dict[str, set[str]]` | — | Return ``{importer path: imported paths}`` for the given Python files. |
| `reverse_closure` | `(start: Iterable[str], incoming: Callable[[str], Iterable[str]]) -> set[str]` | — | Return every path that reaches a start path through incoming edges. |
| `static_selection` | `(root: Path, modules: Iterable[str]) -> set[str]` | — | — |
| `reference_selection` | `(root: Path, paths: Iterable[str]) -> set[str]` | — | Select test files whose text names a changed non-Python file. |
| `wiki_revision` | `(root: Path) -> str` | — | Return the commit the wiki knowledge snapshot was evaluated at. |
| `_require_clean` | `(payload: dict[str, Any], what: str) -> None` | — | — |
| `_impact_one` | `(arguments: tuple[str, str]) -> dict[str, Any]` | — | — |
| `wiki_selection` | `(root: Path, base: str, modules: list[str], graph: WikiGraph \| None = None) -> set[str]` | — | — |
| `select` | `(root: Path, base: str, head: str, *, engine: str = 'wiki', wiki_graph: WikiGraph \| None = None) -> dict[str, Any]` | — | — |
| `existing_tests` | `(root: Path) -> set[str]` | — | — |
| `main` | `(argv: list[str] \| None = None) -> int` | — | — |
