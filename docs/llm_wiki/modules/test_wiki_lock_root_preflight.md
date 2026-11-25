# test_wiki_lock_root_preflight Module

**Path:** `scripts/ci/tests/test_wiki_lock_root_preflight.py`

## Description

Wiki writer preflight refuses checkouts whose lock root leaves the repository.

## Imports

| Source | Symbols |
|--------|---------|
| `contextlib` | `contextlib` |
| `io` | `io` |
| `pathlib` | `Path` |
| `subprocess` | `subprocess` |
| `sys` | `sys` |
| `tempfile` | `tempfile` |
| `unittest` | `unittest` |
| `wiki_lock_root_preflight` | `preflight` |

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
| [WikiLockRootPreflight](../entities/WikiLockRootPreflight.md) | 43 | `unittest.TestCase` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_git` | `(cwd: Path, *args: str) -> None` | — | — |
| `_repository` | `(path: Path) -> Path` | — | — |
| `_wiki` | `(checkout: Path) -> None` | — | — |
| `_run_main` | `(argv)` | — | — |
