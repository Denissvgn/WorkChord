# NativeConnectionApproval

**Location:** `backend/app/routers/identity.py:43`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [routers_identity](../modules/routers_identity.md)

## Description

_Auto-generated from `NativeConnectionApproval` in `backend/app/routers/identity.py`._

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `verification_code` | `str` | `verification_code` | Yes | No | — | pattern='^[A-Z2-9]{4}-[A-Z2-9]{4}$' | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["NativeConnectionApproval (backend/app/routers/identity.py)"]
    n1["BaseModel"]
    n2["approve_native_connection (backend/app/routers/identity.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/routers_identity.md"
    click n2 "../modules/routers_identity.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [routers_identity](../modules/routers_identity.md) | 0 | `verification_code` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `approve_native_connection` | type_reference | [routers_identity](../modules/routers_identity.md) | — |
