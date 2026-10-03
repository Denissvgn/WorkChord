# NativePendingResponse

**Location:** `backend/app/routers/identity.py:65`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [routers_identity](../modules/routers_identity.md)

## Description

_Auto-generated from `NativePendingResponse` in `backend/app/routers/identity.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `status` | `Literal['pending']` | `status` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["NativePendingResponse (backend/app/routers/identity.py)"]
    n1["BaseModel"]
    n2["exchange_native_connection (backend/app/routers/identity.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/routers_identity.md"
    click n2 "../modules/routers_identity.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [routers_identity](../modules/routers_identity.md) | 0 | `status` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `exchange_native_connection` | type_reference | [routers_identity](../modules/routers_identity.md) | — |
