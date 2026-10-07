# TimeEntryCreate

**Location:** `backend/app/schemas/time_entry.py:38`
**Kind:** Pydantic model
**Bases:** `TimeValues`
**Module:** [schemas_time_entry](../modules/schemas_time_entry.md)

## Description

_Auto-generated from `TimeEntryCreate` in `backend/app/schemas/time_entry.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `project_id` | `StrictInt` | `project_id` | Yes | No | — | ge=1 | — | — |
| `task_id` | `StrictInt \| None` | `task_id` | No | Yes | `None` | ge=1 | — | — |
| `request_id` | `UUID` | `request_id` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TimeEntryCreate (backend/app/schemas/time_entry.py)"]
    n1["TimeValues (backend/app/schemas/time_entry.py)"]
    n2["create_entry (backend/app/routers/time_entries.py)"]
    n3["entry_data (backend/tests/test_time_entries.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_time_entry.md"
    click n1 "../modules/schemas_time_entry.md"
    click n2 "../modules/time_entries.md"
    click n3 "../modules/test_time_entries.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_time_entry](../modules/schemas_time_entry.md) | 0 | `project_id`, `request_id`, `task_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `TimeValues` | [schemas_time_entry](../modules/schemas_time_entry.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_entry` | type_reference | [time_entries](../modules/time_entries.md) | — |
| `entry_data` | call | [test_time_entries](../modules/test_time_entries.md) | 1 |
