# SqlStateFailure

**Location:** `backend/tests/database/test_runtime_policy.py:23`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [test_runtime_policy](../modules/test_runtime_policy.md)

## Description

Minimal Psycopg-shaped fault used without a database server.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(sqlstate: str)` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SqlStateFailure (backend/tests/database/test_runtime_policy.py)"]
    n1["RuntimeError"]
    n2["test_retry_classifier_uses_sqlstate_not_messages (backend/tests/database/test_runtime_policy.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/test_runtime_policy.md"
    click n2 "../modules/test_runtime_policy.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [test_runtime_policy](../modules/test_runtime_policy.md) | 1 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `test_retry_classifier_uses_sqlstate_not_messages` | call | [test_runtime_policy](../modules/test_runtime_policy.md) | 1 |
