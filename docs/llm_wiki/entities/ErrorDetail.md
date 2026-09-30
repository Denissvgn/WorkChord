# ErrorDetail

**Location:** `backend/app/schemas/common.py:5`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_common](../modules/schemas_common.md)

## Description

Detail of validation error.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `field` | `str` | `field` | Yes | No | — | — | — | — |
| `message` | `str` | `message` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ErrorDetail (backend/app/schemas/common.py)"]
    n1["BaseModel"]
    n2["handle_validation_error (backend/app/utils/exceptions.py)"]
    n3["ValidationException.__init__ (backend/app/utils/exceptions.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_common.md"
    click n2 "../modules/exceptions.md"
    click n3 "../modules/exceptions.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_common](../modules/schemas_common.md) | 0 | `field`, `message` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `handle_validation_error` | call | [exceptions](../modules/exceptions.md) | 1 |
| `ValidationException.__init__` | type_reference | [exceptions](../modules/exceptions.md) | — |
