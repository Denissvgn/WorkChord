# TaskUnmerge

**Location:** `backend/app/schemas/task.py:268`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task](../modules/schemas_task.md)

## Description

Request schema for unmerging a parent task.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `expected_revision` | `Optional[int]` | `expected_revision` | No | Yes | `None` | ge=1 | — | — |
| `delete_parent` | `bool` | `delete_parent` | No | No | `True` | — | — | Delete the parent task after unmerging |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskUnmerge (backend/app/schemas/task.py)"]
    n1["BaseModel"]
    n2["unmerge_task (backend/app/routers/tasks.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_task.md"
    click n2 "../modules/tasks.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task](../modules/schemas_task.md) | 0 | `delete_parent`, `expected_revision` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `unmerge_task` | type_reference | [tasks](../modules/tasks.md) | — |
