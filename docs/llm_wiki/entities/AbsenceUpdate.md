# AbsenceUpdate

**Location:** `backend/app/routers/capacity.py:27`
**Kind:** Pydantic model
**Bases:** `AbsenceInput`
**Module:** [routers_capacity](../modules/routers_capacity.md)

## Description

_Auto-generated from `AbsenceUpdate` in `backend/app/routers/capacity.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `expected_version` | `int` | `expected_version` | Yes | No | — | gt=0 | — | — |
| `deleted` | `bool` | `deleted` | No | No | `False` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AbsenceUpdate (backend/app/routers/capacity.py)"]
    n1["AbsenceInput (backend/app/routers/capacity.py)"]
    n2["update_absence (backend/app/routers/capacity.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/routers_capacity.md"
    click n1 "../modules/routers_capacity.md"
    click n2 "../modules/routers_capacity.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [routers_capacity](../modules/routers_capacity.md) | 0 | `deleted`, `expected_version` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `AbsenceInput` | [routers_capacity](../modules/routers_capacity.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `update_absence` | type_reference | [routers_capacity](../modules/routers_capacity.md) | — |
