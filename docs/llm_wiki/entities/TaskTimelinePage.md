# TaskTimelinePage

**Location:** `backend/app/schemas/agent.py:466`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

_Auto-generated from `TaskTimelinePage` in `backend/app/schemas/agent.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `task_id` | `int` | `task_id` | Yes | No | — | — | — | — |
| `items` | `list[TaskTimelinePageItem]` | `items` | Yes | No | — | — | — | — |
| `has_more` | `bool` | `has_more` | Yes | No | — | — | — | — |
| `next_cursor` | `str \| None` | `next_cursor` | Yes | Yes | — | — | — | — |
| `limit` | `int` | `limit` | Yes | No | — | — | — | — |
| `consistency` | `str` | `consistency` | No | No | `'live_timestamp_id_desc'` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskTimelinePage (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["get_task_timeline_page (backend/app/routers/tasks.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_agent.md"
    click n2 "../modules/tasks.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 0 | `consistency`, `has_more`, `items`, `limit`, `next_cursor`, `task_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_task_timeline_page` | call | [tasks](../modules/tasks.md) | 1 |
| `get_task_timeline_page` | type_reference | [tasks](../modules/tasks.md) | — |
