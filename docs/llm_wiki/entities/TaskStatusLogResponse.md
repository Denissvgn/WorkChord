# TaskStatusLogResponse

**Location:** `backend/app/schemas/task.py:392`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task](../modules/schemas_task.md)

## Description

Response for task status log entry.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `id` | `int` | `id` | Yes | No | — | — | — | — |
| `task_id` | `int` | `task_id` | Yes | No | — | — | — | — |
| `task_title` | `Optional[str]` | `task_title` | No | Yes | `None` | — | — | — |
| `from_status` | `str` | `from_status` | Yes | No | — | — | — | — |
| `to_status` | `str` | `to_status` | Yes | No | — | — | — | — |
| `changed_at` | `datetime` | `changed_at` | Yes | No | — | — | — | — |
| `reason` | `Optional[str]` | `reason` | No | Yes | `None` | — | — | — |
| `triggered_by` | `str` | `triggered_by` | No | No | `'user'` | — | — | — |
| `affected_task_ids` | `list[int]` | `affected_task_ids` | No | No | `[]` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskStatusLogResponse (backend/app/schemas/task.py)"]
    n1["BaseModel"]
    n2["get_iteration_status_history (backend/app/routers/tasks.py)"]
    n3["get_task_status_history (backend/app/routers/tasks.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_task.md"
    click n2 "../modules/tasks.md"
    click n3 "../modules/tasks.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task](../modules/schemas_task.md) | 0 | `affected_task_ids`, `changed_at`, `from_status`, `id`, `reason`, `task_id`, `task_title`, `to_status`, `triggered_by` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_iteration_status_history` | call | [tasks](../modules/tasks.md) | 1 |
| `get_iteration_status_history` | type_reference | [tasks](../modules/tasks.md) | — |
| `get_task_status_history` | call | [tasks](../modules/tasks.md) | 1 |
| `get_task_status_history` | type_reference | [tasks](../modules/tasks.md) | — |
