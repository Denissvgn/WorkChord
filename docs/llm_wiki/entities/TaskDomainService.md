# TaskDomainService

**Location:** `backend/app/services/task_domain_service.py:157`
**Kind:** Class
**Bases:** —
**Module:** [task_domain_service](../modules/task_domain_service.md)

## Description

_Auto-generated from `TaskDomainService` in `backend/app/services/task_domain_service.py`._

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(db)` | — | — |
| `tasks` | `()` | `@property` | — |
| `ownership` | *(async)* `(task_id, *, lock = False)` | — | — |
| `_policy_task` | *(async)* `(task_id)` | — | — |
| `allowed_actions` | *(async)* `(task_id)` | — | — |
| `command` | *(async)* `(task_id: int, data: TaskActionRequest)` | `@atomic_command` | — |
| `_cancel_execution` | *(async)* `(task, data)` | — | — |
| `_commitment` | *(async)* `(task, data)` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskDomainService (backend/app/services/task_domain_service.py)"]
    n1["apply_task_command (backend/app/mcp_agent_tools.py)"]
    n2["get_task_actions (backend/app/mcp_agent_tools.py)"]
    n3["task_actions (backend/app/routers/task_domain.py)"]
    n4["task_command (backend/app/routers/task_domain.py)"]
    n5["TaskDetailService.my_work (backend/app/services/task_detail_service.py)"]
    n6["test_dependency_requires_current_acceptance_and_blocks_manual_start (backend/tests/test_delivery_dependencies.py)"]
    n7["accepted_work (backend/tests/test_delivery_metrics.py)"]
    n8["test_observations_survive_hierarchy_moves_reopen_and_deletion (backend/tests/test_delivery_metrics.py)"]
    n9["test_deep_ancestor_deferral_clearing_and_unscheduled_manual_freedom (backend/tests/test_effective_deferral.py)"]
    n10["test_reparenting_recomputes_inherited_deferral_without_copying_the_flag (backend/tests/test_effective_deferral.py)"]
    n11["test_stale_session_cannot_ignore_a_committed_ancestor_deferral (backend/tests/test_effective_deferral.py)"]
    n12["test_project_zone_drives_actual_manual_day_and_metric_day (backend/tests/test_project_working_timezone.py)"]
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
    click n0 "../modules/task_domain_service.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_task_domain.md"
    click n4 "../modules/routers_task_domain.md"
    click n5 "../modules/task_detail_service.md"
    click n6 "../modules/test_delivery_dependencies.md"
    click n7 "../modules/test_delivery_metrics.md"
    click n8 "../modules/test_delivery_metrics.md"
    click n9 "../modules/test_effective_deferral.md"
    click n10 "../modules/test_effective_deferral.md"
    click n11 "../modules/test_effective_deferral.md"
    click n12 "../modules/test_project_working_timezone.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [task_domain_service](../modules/task_domain_service.md) | 8 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `apply_task_command` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `get_task_actions` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `task_actions` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `task_command` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `TaskDetailService.my_work` | call | [task_detail_service](../modules/task_detail_service.md) | 1 |
| `test_dependency_requires_current_acceptance_and_blocks_manual_start` | call | [test_delivery_dependencies](../modules/test_delivery_dependencies.md) | 2 |
| `accepted_work` | call | [test_delivery_metrics](../modules/test_delivery_metrics.md) | 2 |
| `test_observations_survive_hierarchy_moves_reopen_and_deletion` | call | [test_delivery_metrics](../modules/test_delivery_metrics.md) | 1 |
| `test_deep_ancestor_deferral_clearing_and_unscheduled_manual_freedom` | call | [test_effective_deferral](../modules/test_effective_deferral.md) | 2 |
| `test_reparenting_recomputes_inherited_deferral_without_copying_the_flag` | call | [test_effective_deferral](../modules/test_effective_deferral.md) | 2 |
| `test_stale_session_cannot_ignore_a_committed_ancestor_deferral` | call | [test_effective_deferral](../modules/test_effective_deferral.md) | 1 |
| `test_project_zone_drives_actual_manual_day_and_metric_day` | call | [test_project_working_timezone](../modules/test_project_working_timezone.md) | 1 |

> References: showing 12 of 21 logical references; 9 omitted by the 12-row generated summary limit.
