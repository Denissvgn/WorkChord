# FallbackRuleTests

**Location:** `scripts/ci/tests/test_select_backend_tests.py:73`
**Kind:** Class
**Bases:** `RepositoryCase`
**Module:** [test_select_backend_tests](../modules/test_select_backend_tests.md)

## Description

_Auto-generated from `FallbackRuleTests` in `scripts/ci/tests/test_select_backend_tests.py`._

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `assert_full` | `(files: dict[str, str], reason: str) -> None` | — | — |
| `test_conftest_anywhere_is_shared_ground` | `() -> None` | — | — |
| `test_nested_conftest_is_shared_ground` | `() -> None` | — | — |
| `test_migrations_models_and_configuration_are_shared_ground` | `() -> None` | — | — |
| `test_ordinary_paths_are_not_shared_ground` | `() -> None` | — | — |
| `test_missing_base_selects_full` | `() -> None` | — | — |
| `test_unknown_commit_selects_full` | `() -> None` | — | — |
| `test_test_data_change_selects_full` | `() -> None` | — | — |
| `test_unparseable_module_selects_full` | `() -> None` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["FallbackRuleTests (scripts/ci/tests/test_select_backend_tests.py)"]
    n1["RepositoryCase (scripts/ci/tests/test_select_backend_tests.py)"]
    n0 --> n1
    click n0 "../modules/test_select_backend_tests.md"
    click n1 "../modules/test_select_backend_tests.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [test_select_backend_tests](../modules/test_select_backend_tests.md) | 9 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RepositoryCase` | [test_select_backend_tests](../modules/test_select_backend_tests.md) |
