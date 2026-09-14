# NotFoundException

**Location:** `backend/app/utils/exceptions.py:20`
**Kind:** Class
**Bases:** `WorkChordException`
**Module:** [exceptions](../modules/exceptions.md)

## Description

Resource not found exception.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(resource: str, id: int)` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["NotFoundException (backend/app/utils/exceptions.py)"]
    n1["WorkChordException (backend/app/utils/exceptions.py)"]
    n2["handle_not_found_exception (backend/app/utils/exceptions.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/exceptions.md"
    click n1 "../modules/exceptions.md"
    click n2 "../modules/exceptions.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [exceptions](../modules/exceptions.md) | 1 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `WorkChordException` | [exceptions](../modules/exceptions.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `handle_not_found_exception` | type_reference | [exceptions](../modules/exceptions.md) | — |
