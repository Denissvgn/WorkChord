# TaskDomainService

**Location:** `backend/app/services/task_domain_service.py:151`
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
    n7["test_backlog_manual_execution_independent_review_and_reopen (backend/tests/test_task_domain.py)"]
    n8["test_cancel_requires_current_execution_ownership_and_invalidates_fence (backend/tests/test_task_domain.py)"]
    n9["test_owner_and_ids_survive_commit_uncommit (backend/tests/test_task_domain.py)"]
    n10["test_progress_availability_matches_open_leaf_execution_permission (backend/tests/test_task_domain.py)"]
    n11["test_rework_requires_fresh_progress_and_preserves_prior_evidence (backend/tests/test_task_domain.py)"]
    n12["test_blocked_metrics_include_explicit_and_canceled_dependencies (backend/tests/test_task_domain_integrity.py)"]
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
    click n7 "../modules/test_task_domain.md"
    click n8 "../modules/test_task_domain.md"
    click n9 "../modules/test_task_domain.md"
    click n10 "../modules/test_task_domain.md"
    click n11 "../modules/test_task_domain.md"
    click n12 "../modules/test_task_domain_integrity.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [task_domain_service](../modules/task_domain_service.md) | 7 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `apply_task_command` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `get_task_actions` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `task_actions` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `task_command` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `TaskDetailService.my_work` | call | [task_detail_service](../modules/task_detail_service.md) | 1 |
| `test_dependency_requires_current_acceptance_and_blocks_manual_start` | call | [test_delivery_dependencies](../modules/test_delivery_dependencies.md) | 2 |
| `test_backlog_manual_execution_independent_review_and_reopen` | call | [test_task_domain](../modules/test_task_domain.md) | 3 |
| `test_cancel_requires_current_execution_ownership_and_invalidates_fence` | call | [test_task_domain](../modules/test_task_domain.md) | 3 |
| `test_owner_and_ids_survive_commit_uncommit` | call | [test_task_domain](../modules/test_task_domain.md) | 2 |
| `test_progress_availability_matches_open_leaf_execution_permission` | call | [test_task_domain](../modules/test_task_domain.md) | 1 |
| `test_rework_requires_fresh_progress_and_preserves_prior_evidence` | call | [test_task_domain](../modules/test_task_domain.md) | 1 |
| `test_blocked_metrics_include_explicit_and_canceled_dependencies` | call | [test_task_domain_integrity](../modules/test_task_domain_integrity.md) | 2 |

> References: showing 12 of 13 logical references; 1 omitted by the 12-row generated summary limit.
