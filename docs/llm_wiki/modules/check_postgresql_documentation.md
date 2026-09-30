# check_postgresql_documentation Module

**Path:** `scripts/ci/check_postgresql_documentation.py`

## Description

Fail closed when the PostgreSQL pre-cutover documentation drifts.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `pathlib` | `Path` |
| `re` | `re` |
| `sys` | `sys` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [DocumentationContractError](../entities/DocumentationContractError.md) | 39 | `RuntimeError` | Raised when an operator-facing contract is incomplete or unsafe. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_read` | `(relative_path: Path) -> str` | — | — |
| `_require` | `(relative_path: Path, *snippets: str) -> None` | — | — |
| `_local_link_count` | `(relative_path: Path) -> int` | — | — |
| `check_documentation` | `() -> tuple[int, int]` | — | — |
| `main` | `() -> int` | — | — |
