# TaskBatchUpdateRequest

**Location:** `backend/app/schemas/task.py:428`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task](../modules/schemas_task.md)

## Description

Schema for updating multiple tasks in a single request.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `tasks` | `list[TaskBatchUpdateItem]` | `tasks` | Yes | No | — | — | — | — |
| `expected_revision` | `Optional[int]` | `expected_revision` | No | Yes | `None` | ge=1 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskBatchUpdateRequest (backend/app/schemas/task.py)"]
    n1["BaseModel"]
    n2["batch_update_tasks (backend/app/routers/tasks.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_task.md"
    click n2 "../modules/tasks.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task](../modules/schemas_task.md) | 0 | `expected_revision`, `tasks` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `batch_update_tasks` | type_reference | [tasks](../modules/tasks.md) | — |
