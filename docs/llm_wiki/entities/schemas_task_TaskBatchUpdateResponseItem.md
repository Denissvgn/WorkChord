# TaskBatchUpdateResponseItem

**Location:** `backend/app/schemas/task.py:411`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task](../modules/schemas_task.md)

## Description

Schema for a single task update response inside a batch response.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `task_id` | `int` | `task_id` | Yes | No | — | — | — | — |
| `success` | `bool` | `success` | Yes | No | — | — | — | — |
| `error` | `Optional[str]` | `error` | No | Yes | `None` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskBatchUpdateResponseItem (backend/app/schemas/task.py)"]
    n1["BaseModel"]
    n2["apply_batch_update_items (backend/app/routers/tasks.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_task.md"
    click n2 "../modules/tasks.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task](../modules/schemas_task.md) | 0 | `error`, `success`, `task_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `apply_batch_update_items` | call | [tasks](../modules/tasks.md) | 1 |
| `apply_batch_update_items` | type_reference | [tasks](../modules/tasks.md) | — |
