# wiki_lock_root_preflight Module

**Path:** `scripts/ci/wiki_lock_root_preflight.py`

## Description

Refuse wiki writer runs whose storage and governance locks would leave this repository.

The installed llm-wiki resolver places its lock root at the nearest real
directory named ``.git`` found by searching upward from the wiki directory
(``docs/llm_wiki``). A linked worktree has a ``.git`` file, and a symlinked
``.git`` is not a real directory, so the resolver skips both and can select an
enclosing repository. This preflight reads Git metadata only. It never opens a
lock and never runs the writer.

Exit status: 0 when the selected lock root is the checkout's own repository,
1 when it is not or cannot be determined.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `argparse` | `argparse` |
| `pathlib` | `Path` |
| `subprocess` | `subprocess` |
| `sys` | `sys` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_git_path` | `(checkout: Path, *args: str) -> Path` | — | — |
| `own_repository_git_dir` | `(checkout: Path) -> Path` | — | Return the shared Git directory the checkout belongs to. |
| `_is_real_git_directory` | `(candidate: Path) -> bool` | — | — |
| `selected_lock_git_dir` | `(wiki_directory: Path) -> Path \| None` | — | Return the nearest real ``.git`` directory searching upward from the wiki directory. |
| `check` | `(checkout: Path) -> tuple[bool, str]` | — | — |
| `main` | `(argv: list[str] \| None = None) -> int` | — | — |
