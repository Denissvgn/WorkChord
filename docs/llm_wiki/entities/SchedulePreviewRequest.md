# SchedulePreviewRequest

**Location:** `backend/app/schemas/gantt.py:103`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_gantt](../modules/schemas_gantt.md)

## Description

Sandbox edits to dry-run through the real scheduler.

``changes`` uses the same item shape as the batch-update endpoint so a
preview exercises exactly the payload a later apply would send.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `changes` | `list[TaskBatchUpdateItem]` | `changes` | No | No | `[]` | — | — | — |
| `expected_revision` | `Optional[int]` | `expected_revision` | No | Yes | `None` | — | — | — |
| `expected_planning_revision` | `Optional[int]` | `expected_planning_revision` | No | Yes | `None` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SchedulePreviewRequest (backend/app/schemas/gantt.py)"]
    n1["BaseModel"]
    n2["preview_iteration_schedule (backend/app/routers/gantt.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_gantt.md"
    click n2 "../modules/routers_gantt.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_gantt](../modules/schemas_gantt.md) | 0 | `changes`, `expected_planning_revision`, `expected_revision` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `preview_iteration_schedule` | type_reference | [routers_gantt](../modules/routers_gantt.md) | — |
