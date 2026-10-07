# TaskTimelineItem

**Location:** `backend/app/schemas/agent.py:445`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

Merged timeline item for a task.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `item_type` | `Literal['task_event', 'status_log', 'agent_run', 'agent_run_event']` | `item_type` | Yes | No | — | — | — | — |
| `timestamp` | `datetime` | `timestamp` | Yes | No | — | — | — | — |
| `title` | `str` | `title` | Yes | No | — | — | — | — |
| `payload` | `dict[str, Any]` | `payload` | No | No | factory: `dict` | — | — | — |
| `actor_type` | `Optional[str]` | `actor_type` | No | Yes | `None` | — | — | — |
| `actor_id` | `Optional[int]` | `actor_id` | No | Yes | `None` | — | — | — |
| `trace_id` | `Optional[str]` | `trace_id` | No | Yes | `None` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskTimelineItem (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["TaskTimelinePageItem (backend/app/schemas/agent.py)"]
    n3["get_task_timeline (backend/app/routers/tasks.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_agent.md"
    click n2 "../modules/schemas_agent.md"
    click n3 "../modules/tasks.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 0 | `actor_id`, `actor_type`, `item_type`, `payload`, `timestamp`, `title`, `trace_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
| Subclass | `TaskTimelinePageItem` | [schemas_agent](../modules/schemas_agent.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_task_timeline` | call | [tasks](../modules/tasks.md) | 1 |
