# WorkChordException

**Location:** `backend/app/utils/exceptions.py:12`
**Kind:** Class
**Bases:** `Exception`
**Module:** [exceptions](../modules/exceptions.md)

## Description

Base exception for the application.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(message: str, code: str = 'error')` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WorkChordException (backend/app/utils/exceptions.py)"]
    n1["Exception"]
    n2["CircularDependencyException (backend/app/utils/exceptions.py)"]
    n3["NotFoundException (backend/app/utils/exceptions.py)"]
    n4["ValidationException (backend/app/utils/exceptions.py)"]
    n5["handle_workchord_exception (backend/app/utils/exceptions.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/exceptions.md"
    click n2 "../modules/exceptions.md"
    click n3 "../modules/exceptions.md"
    click n4 "../modules/exceptions.md"
    click n5 "../modules/exceptions.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [exceptions](../modules/exceptions.md) | 1 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Exception` | — |
| Subclass | `CircularDependencyException` | [exceptions](../modules/exceptions.md) |
| Subclass | `NotFoundException` | [exceptions](../modules/exceptions.md) |
| Subclass | `ValidationException` | [exceptions](../modules/exceptions.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `handle_workchord_exception` | type_reference | [exceptions](../modules/exceptions.md) | — |
