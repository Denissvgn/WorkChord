# CalendarSelection

**Location:** `backend/app/routers/capacity.py:17`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [routers_capacity](../modules/routers_capacity.md)

## Description

_Auto-generated from `CalendarSelection` in `backend/app/routers/capacity.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `calendar_id` | `int` | `calendar_id` | Yes | No | — | gt=0 | — | — |
| `expected_version` | `int` | `expected_version` | Yes | No | — | ge=0 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CalendarSelection (backend/app/routers/capacity.py)"]
    n1["BaseModel"]
    n2["set_availability (backend/app/routers/capacity.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/routers_capacity.md"
    click n2 "../modules/routers_capacity.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [routers_capacity](../modules/routers_capacity.md) | 0 | `calendar_id`, `expected_version` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `set_availability` | type_reference | [routers_capacity](../modules/routers_capacity.md) | — |
