# TaskBatchUpdateResponse

**Location:** `backend/app/schemas/task.py:451`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task](../modules/schemas_task.md)

## Description

Response schema for a batch task update.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `results` | `list[TaskBatchUpdateResponseItem]` | `results` | Yes | No | — | — | — | — |
| `updated_tasks` | `list[TaskResponse]` | `updated_tasks` | Yes | No | — | — | — | — |
| `schedule_result` | `Optional[Any]` | `schedule_result` | No | Yes | `None` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskBatchUpdateResponse (backend/app/schemas/task.py)"]
    n1["BaseModel"]
    n2["apply_batch_update_items (backend/app/routers/tasks.py)"]
    n3["batch_update_tasks (backend/app/routers/tasks.py)"]
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
| [schemas_task](../modules/schemas_task.md) | 0 | `results`, `schedule_result`, `updated_tasks` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `apply_batch_update_items` | type_reference | [tasks](../modules/tasks.md) | — |
| `batch_update_tasks` | call | [tasks](../modules/tasks.md) | 1 |
| `batch_update_tasks` | type_reference | [tasks](../modules/tasks.md) | — |
