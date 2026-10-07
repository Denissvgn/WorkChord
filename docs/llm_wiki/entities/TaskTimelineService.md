# TaskTimelineService

**Location:** `backend/app/services/task_timeline_service.py:16`
**Kind:** Class
**Bases:** —
**Module:** [task_timeline_service](../modules/task_timeline_service.md)

## Description

_Auto-generated from `TaskTimelineService` in `backend/app/services/task_timeline_service.py`._

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(db, serializer = None)` | — | — |
| `decode` | `(cursor, task_id)` | `@staticmethod` | — |
| `page` | *(async)* `(task_id, *, limit = 50, cursor = None)` | — | — |
| `item` | `(source, row, at)` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskTimelineService (backend/app/services/task_timeline_service.py)"]
    n1["get_task_timeline_page (backend/app/routers/tasks.py)"]
    n2["AgentService.get_task_timeline (backend/app/services/agent_service.py)"]
    n3["test_history_pages_ties_and_legacy_bound (backend/tests/test_task_pagination.py)"]
    n4["test_mixed_timeline_sources_have_stable_ties_and_actor_provenance (backend/tests/test_task_pagination.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/task_timeline_service.md"
    click n1 "../modules/tasks.md"
    click n2 "../modules/agent_service.md"
    click n3 "../modules/test_task_pagination.md"
    click n4 "../modules/test_task_pagination.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [task_timeline_service](../modules/task_timeline_service.md) | 4 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_task_timeline_page` | call | [tasks](../modules/tasks.md) | 1 |
| `AgentService.get_task_timeline` | call | [agent_service](../modules/agent_service.md) | 1 |
| `test_history_pages_ties_and_legacy_bound` | call | [test_task_pagination](../modules/test_task_pagination.md) | 1 |
| `test_mixed_timeline_sources_have_stable_ties_and_actor_provenance` | call | [test_task_pagination](../modules/test_task_pagination.md) | 1 |
