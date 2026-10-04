# TaskBriefService

**Location:** `backend/app/services/task_brief_service.py:140`
**Kind:** Class
**Bases:** —
**Module:** [task_brief_service](../modules/task_brief_service.md)

## Description

_Auto-generated from `TaskBriefService` in `backend/app/services/task_brief_service.py`._

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(db)` | — | — |
| `tasks` | `()` | `@property` | — |
| `apply_brief` | *(async)* `(task: Task, brief: TaskBrief, *, provenance = 'structured') -> bool` | — | Apply one canonical representation under the task command's existing fence. |
| `restore_brief` | *(async)* `(task, snapshot)` | — | Keep restored legacy images inside an already adopted canonical boundary. |
| `write` | *(async)* `(task_id, data)` | `@atomic_command` | — |
| `conversion` | *(async)* `(task_id, data)` | — | — |
| `_locked` | *(async)* `(task_id, version)` | — | — |
| `write_progress` | *(async)* `(task_id: int, data: ProgressWrite, *, fenced_submission = False)` | `@atomic_command` | — |
| `require_review` | *(async)* `(task: Task, *, accepting: bool)` | — | One independence and evidence boundary for human and assigned-agent review. |
| `record_review` | *(async)* `(task, *, verdict, reason, evidence = '')` | — | — |
| `review` | *(async)* `(task_id: int, data: TaskReviewWrite)` | `@atomic_command` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskBriefService (backend/app/services/task_brief_service.py)"]
    n1["write_task_brief (backend/app/mcp_agent_tools.py)"]
    n2["convert_task_brief (backend/app/routers/task_domain.py)"]
    n3["record_task_progress (backend/app/routers/task_domain.py)"]
    n4["review_task (backend/app/routers/task_domain.py)"]
    n5["write_task_brief (backend/app/routers/task_domain.py)"]
    n6["AgentWorkService._terminal_work (backend/app/services/agent_work_service.py)"]
    n7["AgentWorkService.review (backend/app/services/agent_work_service.py)"]
    n8["BacklogSnapshotService.restore (backend/app/services/backlog_snapshot_service.py)"]
    n9["SnapshotService.restore (backend/app/services/snapshot_service.py)"]
    n10["TaskDomainService.allowed_actions (backend/app/services/task_domain_service.py)"]
    n11["TaskService.create (backend/app/services/task_service.py)"]
    n12["TaskService.update (backend/app/services/task_service.py)"]
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
    click n0 "../modules/task_brief_service.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/routers_task_domain.md"
    click n3 "../modules/routers_task_domain.md"
    click n4 "../modules/routers_task_domain.md"
    click n5 "../modules/routers_task_domain.md"
    click n6 "../modules/agent_work_service.md"
    click n7 "../modules/agent_work_service.md"
    click n8 "../modules/backlog_snapshot_service.md"
    click n9 "../modules/snapshot_service.md"
    click n10 "../modules/task_domain_service.md"
    click n11 "../modules/task_service.md"
    click n12 "../modules/task_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [task_brief_service](../modules/task_brief_service.md) | 11 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `write_task_brief` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `convert_task_brief` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `record_task_progress` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `review_task` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `write_task_brief` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `AgentWorkService._terminal_work` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `AgentWorkService.review` | call | [agent_work_service](../modules/agent_work_service.md) | 2 |
| `BacklogSnapshotService.restore` | call | [backlog_snapshot_service](../modules/backlog_snapshot_service.md) | 1 |
| `SnapshotService.restore` | call | [snapshot_service](../modules/snapshot_service.md) | 1 |
| `TaskDomainService.allowed_actions` | call | [task_domain_service](../modules/task_domain_service.md) | 2 |
| `TaskService.create` | call | [task_service](../modules/task_service.md) | 1 |
| `TaskService.update` | call | [task_service](../modules/task_service.md) | 1 |

> References: showing 12 of 18 logical references; 6 omitted by the 12-row generated summary limit.
