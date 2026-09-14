# DatabaseConflictError

**Location:** `backend/app/database_runtime.py:46`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [database_runtime](../modules/database_runtime.md)

## Description

A safe mutation exhausted serialization/deadlock retries.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["DatabaseConflictError (backend/app/database_runtime.py)"]
    n1["RuntimeError"]
    n2["_exhausted_error (backend/app/database_runtime.py)"]
    n3["database_conflict_error (backend/app/main.py)"]
    n4["backend/tests/database/test_runtime_policy.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/database_runtime.md"
    click n2 "../modules/database_runtime.md"
    click n3 "../modules/app_main.md"
    click n4 "../modules/test_runtime_policy.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [database_runtime](../modules/database_runtime.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_exhausted_error` | call | [database_runtime](../modules/database_runtime.md) | 1 |
| `database_conflict_error` | type_reference | [app_main](../modules/app_main.md) | — |
| `test_runtime_policy` | import | [test_runtime_policy](../modules/test_runtime_policy.md) | — |
