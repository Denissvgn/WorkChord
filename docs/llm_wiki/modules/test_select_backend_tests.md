# test_select_backend_tests Module

**Path:** `scripts/ci/tests/test_select_backend_tests.py`

## Description

Backend test selection falls back to the full suite on any doubt.

## Imports

| Source | Symbols |
|--------|---------|
| `ast` | `ast` |
| `json` | `json` |
| `pathlib` | `Path` |
| `select_backend_tests` | `selector` |
| `subprocess` | `subprocess` |
| `sys` | `sys` |
| `tempfile` | `tempfile` |
| `unittest` | `unittest` |

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
| [RepositoryCase](../entities/RepositoryCase.md) | 79 | `unittest.TestCase` | — |
| [FallbackRuleTests](../entities/FallbackRuleTests.md) | 102 | `RepositoryCase` | — |
| [StaticSelectionTests](../entities/StaticSelectionTests.md) | 191 | `RepositoryCase` | — |
| [FakeWiki](../entities/FakeWiki.md) | 302 | — | Stands in for llm-wiki: impact and incoming imports from fixed data. |
| [WikiSelectionTests](../entities/WikiSelectionTests.md) | 347 | `RepositoryCase` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_git` | `(cwd: Path, *args: str) -> str` | — | — |
| `_write` | `(root: Path, files: dict[str, str]) -> None` | — | — |
| `_impact` | `(paths: list[str], **overrides) -> dict` | — | — |
| `_imports` | `(*sources: str, resolution: str = 'resolved', **overrides) -> dict` | — | — |
