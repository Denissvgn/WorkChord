# IterationPage

**Location:** `backend/app/schemas/iteration.py:123`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_iteration](../modules/schemas_iteration.md)

## Description

_Auto-generated from `IterationPage` in `backend/app/schemas/iteration.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `items` | `list[IterationResponse]` | `items` | Yes | No | — | — | — | — |
| `has_more` | `bool` | `has_more` | Yes | No | — | — | — | — |
| `next_after_id` | `int \| None` | `next_after_id` | Yes | Yes | — | — | — | — |
| `upper_id` | `int` | `upper_id` | Yes | No | — | — | — | — |
| `consistency` | `str` | `consistency` | No | No | `'live_bounded_id_order'` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["IterationPage (backend/app/schemas/iteration.py)"]
    n1["BaseModel"]
    n2["get_iteration_page (backend/app/routers/iterations.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_iteration.md"
    click n2 "../modules/iterations.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_iteration](../modules/schemas_iteration.md) | 0 | `consistency`, `has_more`, `items`, `next_after_id`, `upper_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_iteration_page` | type_reference | [iterations](../modules/iterations.md) | — |
