# TaskReplacementService

**Location:** `backend/app/services/task_replacement_service.py:229`
**Kind:** Class
**Bases:** —
**Module:** [task_replacement_service](../modules/task_replacement_service.md)

## Description

Records and reads the audited disposition that names which task delivers another task's work. A replacement redoes an original whose runs lack attribution as a separate task from a clean base: the original keeps its history and is withdrawn from delivery counts, its dependents and release membership move, and only the replacement can be accepted. A supersession records that a closed or accepted successor already delivered the original's work, without reopening or re-executing either task. Both cases move dependents, delivery prerequisites, release membership and reactivation requirements so the deliverable is counted once. A supersession also closes a postponed original's postponement.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(db)` | — | — |
| `tasks` | `()` | `@property` | — |
| `get` | *(async)* `(task_id)` | — | — |
| `projection` | *(async)* `(relation, task_id)` | — | — |
| `record` | *(async)* `(original_id, data, *, commit = True)` | `@atomic_command` | Link a fresh replacement to an unaccepted original under one audited decision. |
| `supersede` | *(async)* `(original_id, data, *, commit = True)` | `@atomic_command` | Record that a closed or accepted successor already delivered this original's work. |
| `_close_postponement` | *(async)* `(original, successor, data)` | — | End a postponed original's open postponement: its work is delivered, so nothing is left to wait for. |
| `_require_unused` | *(async)* `(original, replacement)` | — | — |
| `_require_no_live_execution` | *(async)* `(original)` | — | — |
| `_require_supersedable` | *(async)* `(original, successor)` | — | — |
| `_require_eligible` | *(async)* `(original, replacement)` | — | — |
| `_move_dependents` | *(async)* `(original, replacement, *, delivered = False)` | — | Point each dependent at the replacement; prerequisite identity, not dependent work, changes. |
| `_move_requirements` | *(async)* `(original, successor)` | — | Reactivation requirements of open postponements that name the original name the successor. |
| `_move_releases` | *(async)* `(original, replacement, *, statuses = ('planned', 'building'))` | — | Releases that planned the original's deliverable count the replacement instead. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskReplacementService (backend/app/services/task_replacement_service.py)"]
    n1["get_task_replacement (backend/app/mcp_agent_tools.py)"]
    n2["record_task_replacement (backend/app/routers/task_domain.py)"]
    n3["record_task_supersession (backend/app/routers/task_domain.py)"]
    n4["task_replacement (backend/app/routers/task_domain.py)"]
    n5["backend/app/services/agent_planning_service.py"]
    n6["_replaced_pair (backend/tests/test_task_replacement.py)"]
    n7["test_a_chained_replacement_inherits_the_earlier_carried_work (backend/tests/test_task_replacement.py)"]
    n8["test_an_owner_override_cannot_accept_a_held_replacement_so_no_next_step_offers_it (backend/tests/test_task_replacement.py)"]
    n9["test_clean_replacement_is_accepted_once_and_carried_work_stays_held (backend/tests/test_task_replacement.py)"]
    n10["test_held_replacement_is_refused_acceptance_without_the_strict_policy (backend/tests/test_task_replacement.py)"]
    n11["test_only_a_project_manager_or_pm_actor_decides (backend/tests/test_task_replacement.py)"]
    n12["test_replacement_refuses_ineligible_pairs (backend/tests/test_task_replacement.py)"]
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
    click n0 "../modules/task_replacement_service.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/routers_task_domain.md"
    click n3 "../modules/routers_task_domain.md"
    click n4 "../modules/routers_task_domain.md"
    click n5 "../modules/agent_planning_service.md"
    click n6 "../modules/test_task_replacement.md"
    click n7 "../modules/test_task_replacement.md"
    click n8 "../modules/test_task_replacement.md"
    click n9 "../modules/test_task_replacement.md"
    click n10 "../modules/test_task_replacement.md"
    click n11 "../modules/test_task_replacement.md"
    click n12 "../modules/test_task_replacement.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [task_replacement_service](../modules/task_replacement_service.md) | 14 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_task_replacement` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `record_task_replacement` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `record_task_supersession` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `task_replacement` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `agent_planning_service` | import | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `_replaced_pair` | call | [test_task_replacement](../modules/test_task_replacement.md) | 1 |
| `test_a_chained_replacement_inherits_the_earlier_carried_work` | call | [test_task_replacement](../modules/test_task_replacement.md) | 1 |
| `test_an_owner_override_cannot_accept_a_held_replacement_so_no_next_step_offers_it` | call | [test_task_replacement](../modules/test_task_replacement.md) | 1 |
| `test_clean_replacement_is_accepted_once_and_carried_work_stays_held` | call | [test_task_replacement](../modules/test_task_replacement.md) | 2 |
| `test_held_replacement_is_refused_acceptance_without_the_strict_policy` | call | [test_task_replacement](../modules/test_task_replacement.md) | 2 |
| `test_only_a_project_manager_or_pm_actor_decides` | call | [test_task_replacement](../modules/test_task_replacement.md) | 1 |
| `test_replacement_refuses_ineligible_pairs` | call | [test_task_replacement](../modules/test_task_replacement.md) | 1 |

> References: showing 12 of 14 logical references; 2 omitted by the 12-row generated summary limit.
