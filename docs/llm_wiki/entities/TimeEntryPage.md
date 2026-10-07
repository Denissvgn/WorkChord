# TimeEntryPage

**Location:** `backend/app/schemas/time_entry.py:76`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_time_entry](../modules/schemas_time_entry.md)

## Description

_Auto-generated from `TimeEntryPage` in `backend/app/schemas/time_entry.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `items` | `list[TimeEntryResponse]` | `items` | Yes | No | — | — | — | — |
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
    n0["TimeEntryPage (backend/app/schemas/time_entry.py)"]
    n1["BaseModel"]
    n2["list_entries (backend/app/routers/time_entries.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_time_entry.md"
    click n2 "../modules/time_entries.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_time_entry](../modules/schemas_time_entry.md) | 0 | `consistency`, `has_more`, `items`, `next_after_id`, `upper_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `list_entries` | type_reference | [time_entries](../modules/time_entries.md) | — |
