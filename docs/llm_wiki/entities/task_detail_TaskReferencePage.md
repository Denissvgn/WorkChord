# TaskReferencePage

**Location:** `backend/app/schemas/task_detail.py:19`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [task_detail](../modules/task_detail.md)

## Description

_Auto-generated from `TaskReferencePage` in `backend/app/schemas/task_detail.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `items` | `list[TaskReference]` | `items` | Yes | No | — | — | — | — |
| `has_more` | `bool` | `has_more` | Yes | No | — | — | — | — |
| `next_after_id` | `int \| None` | `next_after_id` | Yes | Yes | — | — | — | — |
| `limit` | `int` | `limit` | Yes | No | — | — | — | — |
| `consistency` | `str` | `consistency` | No | No | `'live'` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskReferencePage (backend/app/schemas/task_detail.py)"]
    n1["BaseModel"]
    n2["lookup_tasks (backend/app/routers/task_domain.py)"]
    n3["task_review_queue (backend/app/routers/task_domain.py)"]
    n4["TaskDetailService.page (backend/app/services/task_detail_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/task_detail.md"
    click n2 "../modules/routers_task_domain.md"
    click n3 "../modules/routers_task_domain.md"
    click n4 "../modules/task_detail_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [task_detail](../modules/task_detail.md) | 0 | `consistency`, `has_more`, `items`, `limit`, `next_after_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `lookup_tasks` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `task_review_queue` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `TaskDetailService.page` | call | [task_detail_service](../modules/task_detail_service.md) | 1 |
