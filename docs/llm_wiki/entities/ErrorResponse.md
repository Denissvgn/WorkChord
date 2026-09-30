# ErrorResponse

**Location:** `backend/app/schemas/common.py:11`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_common](../modules/schemas_common.md)

## Description

Standard error response.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `code` | `str` | `code` | Yes | No | — | — | — | — |
| `message` | `str` | `message` | Yes | No | — | — | — | — |
| `details` | `list[ErrorDetail]` | `details` | No | No | `[]` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ErrorResponse (backend/app/schemas/common.py)"]
    n1["BaseModel"]
    n2["backend/app/schemas/__init__.py"]
    n3["handle_integrity_error (backend/app/utils/exceptions.py)"]
    n4["handle_not_found_exception (backend/app/utils/exceptions.py)"]
    n5["handle_validation_error (backend/app/utils/exceptions.py)"]
    n6["handle_workchord_exception (backend/app/utils/exceptions.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/schemas_common.md"
    click n2 "../modules/schemas___init__.md"
    click n3 "../modules/exceptions.md"
    click n4 "../modules/exceptions.md"
    click n5 "../modules/exceptions.md"
    click n6 "../modules/exceptions.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_common](../modules/schemas_common.md) | 0 | `code`, `details`, `message` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `handle_integrity_error` | call | [exceptions](../modules/exceptions.md) | 1 |
| `handle_not_found_exception` | call | [exceptions](../modules/exceptions.md) | 1 |
| `handle_validation_error` | call | [exceptions](../modules/exceptions.md) | 1 |
| `handle_workchord_exception` | call | [exceptions](../modules/exceptions.md) | 1 |
