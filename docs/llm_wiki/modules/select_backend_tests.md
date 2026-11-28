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
     components). Deleted non-Python paths are traced the same way.

   Test files reached this way are selected.
5. The always-run set is added. When the result covers every backend test,
   the mode is ``full``.

``--engine wiki`` also queries the llm-wiki knowledge graph (``impact`` on the
changed backend modules, then incoming ``imports`` edges from the committed
snapshot) and unions it with the static selection. It falls back to ``full``
when the wiki snapshot revision is not an ancestor of (or equal to) the base,
when llm-wiki is not importable, or when a result is truncated, ambiguous,
unresolved, not ``ready`` or reports ``found: false`` for a changed module.

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
| `re` | `re` |
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
| [FullSuite](../entities/FullSuite.md) | 142 | `Exception` | Raised when the selection must fall back to the full suite. |
| [Repository](../entities/Repository.md) | 299 | — | The Python files of the head checkout and how they depend on each other. |
| [WikiGraph](../entities/WikiGraph.md) | 466 | — | Read-only llm-wiki queries; never syncs or writes the wiki. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_git` | `(root: Path, *args: str) -> subprocess.CompletedProcess[str]` | — | — |
| `_rev_parse` | `(root: Path, revision: str) -> str` | — | — |
| `require_checkout_at` | `(root: Path, head: str) -> None` | — | The graph is read from the working tree; it must be the head commit. |
| `changed_paths` | `(root: Path, base: str, head: str) -> dict[str, str]` | — | Return ``{path: status}`` for the change from the merge base to head. |
| `tracked_files` | `(root: Path) -> list[str]` | — | — |
| `is_ancestor` | `(root: Path, ancestor: str, descendant: str) -> bool` | — | — |
| `is_shared_ground` | `(path: str) -> bool` | — | Return True when a change to ``path`` can affect any backend test. |
| `is_test_file` | `(path: str) -> bool` | — | — |
| `module_name` | `(path: str) -> str \| None` | — | Map a repository path to its importable module name, or None. |
| `_imported_names` | `(tree: ast.AST, own_module: str, is_package: bool) -> set[str]` | — | — |
| `_tokens` | `(text: str) -> set[str]` | — | Return the path and dotted-name words of ``text`` and their parts. |
| `reverse_closure` | `(start: Iterable[str], incoming: Callable[[str], Iterable[str]]) -> set[str]` | — | Return every path that reaches a start path through incoming edges. |
| `wiki_revision` | `(root: Path) -> str` | — | Return the commit the wiki knowledge snapshot was evaluated at. |
| `_require_clean` | `(payload: dict[str, Any], what: str) -> None` | — | — |
| `_impact_one` | `(arguments: tuple[str, str]) -> dict[str, Any]` | — | — |
| `wiki_selection` | `(root: Path, base: str, modules: list[str], graph: WikiGraph \| None = None) -> set[str]` | — | — |
| `selection_for` | `(repository: Repository, changes: dict[str, str]) -> tuple[set[str], dict[str, list[str]]]` | — | Return the tests a change selects (always-run set excluded) and why. |
| `select` | `(root: Path, base: str, head: str, *, engine: str = 'ast', wiki_graph: WikiGraph \| None = None) -> dict[str, Any]` | — | — |
| `main` | `(argv: list[str] \| None = None) -> int` | — | — |
