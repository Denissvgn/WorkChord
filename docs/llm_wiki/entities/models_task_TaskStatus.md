# TaskStatus

**Location:** `backend/app/models/task.py:30`
**Kind:** Enum
**Bases:** `str`, `Enum`
**Module:** [models_task](../modules/models_task.md)

## Description

Task status enumeration for work tracking.

Workflow: PLANNED -> ACTIVE -> RESOLVED -> CLOSED
- PLANNED: Auto-assigned on task creation
- ACTIVE: Work has started
- RESOLVED: Work completed, pending validation
- CLOSED: Fully completed and validated

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `PLANNED` | `'planned'` | — |
| `ACTIVE` | `'active'` | — |
| `RESOLVED` | `'resolved'` | — |
| `CLOSED` | `'closed'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskStatus (backend/app/models/task.py)"]
    n1["Enum"]
    n2["str"]
    n3["backend/app/models/__init__.py"]
    n4["backend/app/services/agent_readiness.py"]
    n5["backend/app/services/agent_routing_service.py"]
    n6["backend/app/services/agent_service.py"]
    n7["backend/app/services/agent_work_service.py"]
    n8["GitHubStatusAutomationService.apply_rules (backend/app/services/github_status_automation_service.py)"]
    n9["backend/app/services/iteration_service.py"]
    n10["backend/app/services/project_service.py"]
    n11["backend/app/services/scheduler_service.py"]
    n12["TaskBulkOperationService._build_update (backend/app/services/task_bulk_operation_service.py)"]
    n13["TaskBulkOperationService._status_transition_error (backend/app/services/task_bulk_operation_service.py)"]
    n14["TaskService.change_status (backend/app/services/task_service.py)"]
    n0 --> n1
    n0 --> n2
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
    n13 --> n0
    n14 --> n0
    click n0 "../modules/models_task.md"
    click n3 "../modules/models___init__.md"
    click n4 "../modules/agent_readiness.md"
    click n5 "../modules/agent_routing_service.md"
    click n6 "../modules/agent_service.md"
    click n7 "../modules/agent_work_service.md"
    click n8 "../modules/github_status_automation_service.md"
    click n9 "../modules/iteration_service.md"
    click n10 "../modules/project_service.md"
    click n11 "../modules/scheduler_service.md"
    click n12 "../modules/task_bulk_operation_service.md"
    click n13 "../modules/task_bulk_operation_service.md"
    click n14 "../modules/task_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_task](../modules/models_task.md) | 0 | `ACTIVE`, `CLOSED`, `PLANNED`, `RESOLVED` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Enum` | — |
| Base | `str` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `agent_readiness` | import | [agent_readiness](../modules/agent_readiness.md) | — |
| `agent_routing_service` | import | [agent_routing_service](../modules/agent_routing_service.md) | — |
| `agent_service` | import | [agent_service](../modules/agent_service.md) | — |
| `agent_work_service` | import | [agent_work_service](../modules/agent_work_service.md) | — |
| `GitHubStatusAutomationService.apply_rules` | call | [github_status_automation_service](../modules/github_status_automation_service.md) | 1 |
| `iteration_service` | import | [iteration_service](../modules/iteration_service.md) | — |
| `project_service` | import | [project_service](../modules/project_service.md) | — |
| `scheduler_service` | import | [scheduler_service](../modules/scheduler_service.md) | — |
| `TaskBulkOperationService._build_update` | call | [task_bulk_operation_service](../modules/task_bulk_operation_service.md) | 1 |
| `TaskBulkOperationService._status_transition_error` | type_reference | [task_bulk_operation_service](../modules/task_bulk_operation_service.md) | — |
| `TaskService.change_status` | type_reference | [task_service](../modules/task_service.md) | — |

> References: showing 12 of 13 logical references; 1 omitted by the 12-row generated summary limit.
