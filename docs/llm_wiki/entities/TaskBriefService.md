# TaskBriefService

**Location:** `backend/app/services/task_brief_service.py:208`
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
| `apply_brief` | *(async)* `(task: Task, brief: TaskBrief, *, provenance = 'structured', enforce = True, resolve_routing = True) -> bool` | — | Apply one canonical representation under the task command's existing fence. |
| `restore_brief` | *(async)* `(task, snapshot)` | — | Keep restored legacy images inside an already adopted canonical boundary. |
| `write` | *(async)* `(task_id, data)` | `@atomic_command` | — |
| `conversion` | *(async)* `(task_id, data)` | — | — |
| `routing_check` | *(async)* `(task_id, assignee_id = None, *, use_current_assignee = True)` | — | Check the task's routing for its current or a proposed assignee without changing anything. |
| `routing_conversion` | *(async)* `(task_id, data)` | — | Preview or apply moving routing that a brief carries as text into its structured routing. |
| `_locked` | *(async)* `(task_id, version)` | — | — |
| `write_progress` | *(async)* `(task_id: int, data: ProgressWrite, *, fenced_submission = False)` | `@atomic_command` | — |
| `require_review` | *(async)* `(task: Task, *, accepting: bool)` | — | One independence and evidence boundary for human and assigned-agent review. |
| `record_review` | *(async)* `(task, *, reviewed_task_version, verdict, reason, evidence = '')` | — | — |
| `owner_accept` | *(async)* `(task_id: int, data: OwnerAcceptanceWrite)` | — | Accept one resolved task as an owner override of publisher independence. |
| `_owner_accept` | *(async)* `(task_id, data, reason)` | `@atomic_command` | — |
| `review` | *(async)* `(task_id: int, data: TaskReviewWrite)` | `@atomic_command` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskBriefService (backend/app/services/task_brief_service.py)"]
    n1["check_task_routing (backend/app/mcp_agent_tools.py)"]
    n2["convert_task_routing (backend/app/mcp_agent_tools.py)"]
    n3["write_task_brief (backend/app/mcp_agent_tools.py)"]
    n4["check_task_routing (backend/app/routers/task_domain.py)"]
    n5["convert_task_brief (backend/app/routers/task_domain.py)"]
    n6["convert_task_routing (backend/app/routers/task_domain.py)"]
    n7["owner_accept_task (backend/app/routers/task_domain.py)"]
    n8["record_task_progress (backend/app/routers/task_domain.py)"]
    n9["review_task (backend/app/routers/task_domain.py)"]
    n10["write_task_brief (backend/app/routers/task_domain.py)"]
    n11["AgentWorkService._terminal_work (backend/app/services/agent_work_service.py)"]
    n12["AgentWorkService.review (backend/app/services/agent_work_service.py)"]
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
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/mcp_agent_tools.md"
    click n4 "../modules/routers_task_domain.md"
    click n5 "../modules/routers_task_domain.md"
    click n6 "../modules/routers_task_domain.md"
    click n7 "../modules/routers_task_domain.md"
    click n8 "../modules/routers_task_domain.md"
    click n9 "../modules/routers_task_domain.md"
    click n10 "../modules/routers_task_domain.md"
    click n11 "../modules/agent_work_service.md"
    click n12 "../modules/agent_work_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [task_brief_service](../modules/task_brief_service.md) | 15 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `check_task_routing` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `convert_task_routing` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `write_task_brief` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `check_task_routing` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `convert_task_brief` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `convert_task_routing` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `owner_accept_task` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `record_task_progress` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `review_task` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `write_task_brief` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `AgentWorkService._terminal_work` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `AgentWorkService.review` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |

> References: showing 12 of 41 logical references; 29 omitted by the 12-row generated summary limit.
