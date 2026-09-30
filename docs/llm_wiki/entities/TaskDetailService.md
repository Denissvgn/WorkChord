# TaskDetailService

**Location:** `backend/app/services/task_detail_service.py:12`
**Kind:** Class
**Bases:** —
**Module:** [task_detail_service](../modules/task_detail_service.md)

## Description

_Auto-generated from `TaskDetailService` in `backend/app/services/task_detail_service.py`._

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(db)` | — | — |
| `references` | `()` | `@staticmethod` | — |
| `page` | *(async)* `(query, *, limit = 50, after_id = 0)` | — | — |
| `lookup` | *(async)* `(*, project_id = None, iteration_id = None, query = None, backlog_only = False, limit = 50, after_id = 0)` | — | — |
| `detail` | *(async)* `(task_id, *, limit = 50, children_after_id = 0, dependencies_after_id = 0)` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskDetailService (backend/app/services/task_detail_service.py)"]
    n1["get_task_detail (backend/app/mcp_agent_tools.py)"]
    n2["lookup_tasks (backend/app/routers/task_domain.py)"]
    n3["task_detail (backend/app/routers/task_domain.py)"]
    n4["task_review_queue (backend/app/routers/task_domain.py)"]
    n5["task_reviews (backend/app/routers/task_domain.py)"]
    n6["test_bounded_detail_does_not_populate_execution_children (backend/tests/test_task_domain.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/task_detail_service.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/routers_task_domain.md"
    click n3 "../modules/routers_task_domain.md"
    click n4 "../modules/routers_task_domain.md"
    click n5 "../modules/routers_task_domain.md"
    click n6 "../modules/test_task_domain.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [task_detail_service](../modules/task_detail_service.md) | 5 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_task_detail` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `lookup_tasks` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `task_detail` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `task_review_queue` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `task_reviews` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `test_bounded_detail_does_not_populate_execution_children` | call | [test_task_domain](../modules/test_task_domain.md) | 2 |
