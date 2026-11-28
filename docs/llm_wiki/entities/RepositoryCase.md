# RepositoryCase

**Location:** `scripts/ci/tests/test_select_backend_tests.py:79`
**Kind:** Class
**Bases:** `unittest.TestCase`
**Module:** [test_select_backend_tests](../modules/test_select_backend_tests.md)

## Description

_Auto-generated from `RepositoryCase` in `scripts/ci/tests/test_select_backend_tests.py`._

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `setUp` | `() -> None` | — | — |
| `tearDown` | `() -> None` | — | — |
| `change` | `(files: dict[str, str]) -> str` | — | — |
| `select` | `(head: str, **kwargs)` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RepositoryCase (scripts/ci/tests/test_select_backend_tests.py)"]
    n1["unittest.TestCase"]
    n2["FallbackRuleTests (scripts/ci/tests/test_select_backend_tests.py)"]
    n3["StaticSelectionTests (scripts/ci/tests/test_select_backend_tests.py)"]
    n4["WikiSelectionTests (scripts/ci/tests/test_select_backend_tests.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/test_select_backend_tests.md"
    click n2 "../modules/test_select_backend_tests.md"
    click n3 "../modules/test_select_backend_tests.md"
    click n4 "../modules/test_select_backend_tests.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [test_select_backend_tests](../modules/test_select_backend_tests.md) | 4 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `unittest.TestCase` | — |
| Subclass | `FallbackRuleTests` | [test_select_backend_tests](../modules/test_select_backend_tests.md) |
| Subclass | `StaticSelectionTests` | [test_select_backend_tests](../modules/test_select_backend_tests.md) |
| Subclass | `WikiSelectionTests` | [test_select_backend_tests](../modules/test_select_backend_tests.md) |
