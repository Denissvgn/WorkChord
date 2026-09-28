# CascadeUpdateInfo

**Location:** `backend/app/schemas/task.py:403`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task](../modules/schemas_task.md)

## Description

Information about cascading date updates.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `task_id` | `int` | `task_id` | Yes | No | — | — | — | — |
| `task_title` | `str` | `task_title` | Yes | No | — | — | — | — |
| `old_start_date` | `Optional[date]` | `old_start_date` | Yes | Yes | — | — | — | — |
| `new_start_date` | `Optional[date]` | `new_start_date` | Yes | Yes | — | — | — | — |
| `old_end_date` | `Optional[date]` | `old_end_date` | Yes | Yes | — | — | — | — |
| `new_end_date` | `Optional[date]` | `new_end_date` | Yes | Yes | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CascadeUpdateInfo (backend/app/schemas/task.py)"]
    n1["BaseModel"]
    n2["change_task_status (backend/app/routers/tasks.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_task.md"
    click n2 "../modules/tasks.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task](../modules/schemas_task.md) | 0 | `new_end_date`, `new_start_date`, `old_end_date`, `old_start_date`, `task_id`, `task_title` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `change_task_status` | call | [tasks](../modules/tasks.md) | 1 |
