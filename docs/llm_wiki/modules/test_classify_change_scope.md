# test_classify_change_scope Module

**Path:** `scripts/ci/tests/test_classify_change_scope.py`

## Description

Documentation-only classification skips CI only for unchecked documentation.

## Imports

| Source | Symbols |
|--------|---------|
| `classify_change_scope` | `scope` |
| `os` | `os` |
| `pathlib` | `Path` |
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
| [PathRules](../entities/PathRules.md) | 22 | `unittest.TestCase` | — |
| [GitClassification](../entities/GitClassification.md) | 54 | `unittest.TestCase` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_git` | `(cwd: Path, *args: str) -> str` | — | — |
