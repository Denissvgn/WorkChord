# DB

**Location:** `backend/app/routers/task_domain.py:22`
**Kind:** Type alias
**Bases:** —
**Module:** [routers_task_domain](../modules/routers_task_domain.md)
**Target:** `Annotated[AsyncSession, Depends(get_db, scope='function')]`

## Description

_Auto-generated from `DB` in `backend/app/routers/task_domain.py`._

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["DB (backend/app/routers/task_domain.py)"]
    n1["backlog_snapshots (backend/app/routers/task_domain.py)"]
    n2["convert_task_brief (backend/app/routers/task_domain.py)"]
    n3["create_backlog_task (backend/app/routers/task_domain.py)"]
    n4["current_task_review (backend/app/routers/task_domain.py)"]
    n5["delivery_metrics (backend/app/routers/task_domain.py)"]
    n6["human_my_work (backend/app/routers/task_domain.py)"]
    n7["lookup_tasks (backend/app/routers/task_domain.py)"]
    n8["record_task_progress (backend/app/routers/task_domain.py)"]
    n9["restore_backlog (backend/app/routers/task_domain.py)"]
    n10["review_task (backend/app/routers/task_domain.py)"]
    n11["task_actions (backend/app/routers/task_domain.py)"]
    n12["task_brief_history (backend/app/routers/task_domain.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    click n0 "../modules/routers_task_domain.md"
    click n1 "../modules/routers_task_domain.md"
    click n2 "../modules/routers_task_domain.md"
    click n3 "../modules/routers_task_domain.md"
    click n4 "../modules/routers_task_domain.md"
    click n5 "../modules/routers_task_domain.md"
    click n6 "../modules/routers_task_domain.md"
    click n7 "../modules/routers_task_domain.md"
    click n8 "../modules/routers_task_domain.md"
    click n9 "../modules/routers_task_domain.md"
    click n10 "../modules/routers_task_domain.md"
    click n11 "../modules/routers_task_domain.md"
    click n12 "../modules/routers_task_domain.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [routers_task_domain](../modules/routers_task_domain.md) | 0 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `backlog_snapshots` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `convert_task_brief` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `create_backlog_task` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `current_task_review` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `delivery_metrics` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `human_my_work` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `lookup_tasks` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `record_task_progress` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `restore_backlog` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `review_task` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `task_actions` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `task_brief_history` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |

> References: showing 12 of 21 logical references; 9 omitted by the 12-row generated summary limit.
