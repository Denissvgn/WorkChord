# TaskTextContext

**Location:** `backend/app/schemas/task.py:344`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task](../modules/schemas_task.md)

## Description

One text editing base and its observed iteration revision.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `text` | `str` | `text` | Yes | No | — | — | — | — |
| `iteration_id` | `int` | `iteration_id` | Yes | No | — | — | — | — |
| `iteration_revision` | `int` | `iteration_revision` | Yes | No | — | ge=1 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskTextContext (backend/app/schemas/task.py)"]
    n1["BaseModel"]
    n2["get_tasks_text_context (backend/app/routers/tasks.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_task.md"
    click n2 "../modules/tasks.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task](../modules/schemas_task.md) | 0 | `iteration_id`, `iteration_revision`, `text` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_tasks_text_context` | call | [tasks](../modules/tasks.md) | 1 |
| `get_tasks_text_context` | type_reference | [tasks](../modules/tasks.md) | — |
