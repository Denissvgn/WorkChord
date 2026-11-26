# DeliveryDependencyService

**Location:** `backend/app/services/delivery_dependency_service.py:14`
**Kind:** Class
**Bases:** —
**Module:** [delivery_dependency_service](../modules/delivery_dependency_service.md)

## Description

Shared delivery policy for authorized endpoint commands, global cycle checks, current attributed acceptance, generic private-target blockers and transactional downstream invalidation.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(db)` | — | — |
| `graph` | *(async)* `()` | — | Only identifiers enter the internal graph; no hidden work is serialized. |
| `validate_cycles` | *(async)* `()` | — | — |
| `projection` | *(async)* `(task_id)` | — | — |
| `holds` | *(async)* `(task_id)` | — | Prerequisites that keep a task from starting, each with its reason and next owner. |
| `_merge_evidence` | *(async)* `(target, branch)` | — | Read stored pull request observations only; this never calls GitHub. |
| `_hold` | `(target, branch, accepted, merge, reason)` | `@staticmethod` | Name who acts next for a prerequisite that needs accepted code on a branch. |
| `_accepted` | *(async)* `(kind, target)` | — | — |
| `ready` | *(async)* `(task_id)` | — | — |
| `add` | *(async)* `(task_id, kind, target_id, expected_version, target_branch = None)` | `@atomic_command` | — |
| `retarget` | *(async)* `(task_id, edge_id, expected_version, target_branch)` | `@atomic_command` | Change or clear the branch on which a prerequisite's accepted code must be merged. |
| `_change_branch` | *(async)* `(service, task, edge, kind, target_branch, expected_version)` | — | Retarget one existing prerequisite, record it on the task timeline and re-evaluate dependents. |
| `_branch` | `(value, kind)` | `@staticmethod` | — |
| `remove` | *(async)* `(task_id, edge_id, expected_version)` | `@atomic_command` | — |
| `require_unreferenced` | *(async)* `(task_ids = (), milestone_id = None)` | — | — |
| `reconcile` | *(async)* `()` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["DeliveryDependencyService (backend/app/services/delivery_dependency_service.py)"]
    n1["command_transaction (backend/app/commands.py)"]
    n2["list_delivery_dependencies (backend/app/mcp_agent_tools.py)"]
    n3["add_delivery_dependency (backend/app/routers/delivery_dependencies.py)"]
    n4["list_delivery_dependencies (backend/app/routers/delivery_dependencies.py)"]
    n5["remove_delivery_dependency (backend/app/routers/delivery_dependencies.py)"]
    n6["retarget_delivery_dependency (backend/app/routers/delivery_dependencies.py)"]
    n7["batch_update_tasks (backend/app/routers/tasks.py)"]
    n8["backend/app/services/agent_planning_service.py"]
    n9["AgentService.get_pipeline (backend/app/services/agent_service.py)"]
    n10["AgentWorkService._start_blockers (backend/app/services/agent_work_service.py)"]
    n11["AgentWorkService.get_task_context (backend/app/services/agent_work_service.py)"]
    n12["BacklogSnapshotService.restore (backend/app/services/backlog_snapshot_service.py)"]
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
    click n0 "../modules/delivery_dependency_service.md"
    click n1 "../modules/commands.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/delivery_dependencies.md"
    click n4 "../modules/delivery_dependencies.md"
    click n5 "../modules/delivery_dependencies.md"
    click n6 "../modules/delivery_dependencies.md"
    click n7 "../modules/tasks.md"
    click n8 "../modules/agent_planning_service.md"
    click n9 "../modules/agent_service.md"
    click n10 "../modules/agent_work_service.md"
    click n11 "../modules/agent_work_service.md"
    click n12 "../modules/backlog_snapshot_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [delivery_dependency_service](../modules/delivery_dependency_service.md) | 16 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `command_transaction` | call | [commands](../modules/commands.md) | 1 |
| `list_delivery_dependencies` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `add_delivery_dependency` | call | [delivery_dependencies](../modules/delivery_dependencies.md) | 1 |
| `list_delivery_dependencies` | call | [delivery_dependencies](../modules/delivery_dependencies.md) | 1 |
| `remove_delivery_dependency` | call | [delivery_dependencies](../modules/delivery_dependencies.md) | 1 |
| `retarget_delivery_dependency` | call | [delivery_dependencies](../modules/delivery_dependencies.md) | 1 |
| `batch_update_tasks` | call | [tasks](../modules/tasks.md) | 1 |
| `agent_planning_service` | import | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `AgentService.get_pipeline` | call | [agent_service](../modules/agent_service.md) | 1 |
| `AgentWorkService._start_blockers` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `AgentWorkService.get_task_context` | call | [agent_work_service](../modules/agent_work_service.md) | 1 |
| `BacklogSnapshotService.restore` | call | [backlog_snapshot_service](../modules/backlog_snapshot_service.md) | 1 |

> References: showing 12 of 39 logical references; 27 omitted by the 12-row generated summary limit.
