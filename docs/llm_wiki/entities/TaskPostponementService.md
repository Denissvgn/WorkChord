# TaskPostponementService

**Location:** `backend/app/services/task_postponement_service.py:171`
**Kind:** Class
**Bases:** —
**Module:** [task_postponement_service](../modules/task_postponement_service.md)

## Description

_Auto-generated from `TaskPostponementService` in `backend/app/services/task_postponement_service.py`._

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(db)` | — | — |
| `tasks` | `()` | `@property` | — |
| `get` | *(async)* `(task_id)` | — | The task with its open postponement, or its most recent one. |
| `projection` | *(async)* `(task_id, postponement)` | — | — |
| `_locked_task` | *(async)* `(task_id, expected_version)` | — | — |
| `postpone` | *(async)* `(task_id, data, *, commit = True)` | `@atomic_command` | Stop planned, active or resolved leaf work until its requirements are met. |
| `reactivate` | *(async)* `(task_id, data, *, trigger = 'command', commit = True)` | `@atomic_command` | Return postponed work to planned, or to resolved if it was postponed after resolution. |
| `resume` | *(async)* `(task, postponement, *, reason, trigger, expected_version, automatic = False, event_extra = None)` | — | Move locked postponed work back to planned or resolved and close its postponement. |
| `_requirements` | *(async)* `(task, items)` | — | Validate each requirement against current facts; refuse one that can never or already holds. |
| `_timezone` | *(async)* `(task)` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskPostponementService (backend/app/services/task_postponement_service.py)"]
    n1["postpone_task (backend/app/routers/task_domain.py)"]
    n2["reactivate_task (backend/app/routers/task_domain.py)"]
    n3["task_postponement (backend/app/routers/task_domain.py)"]
    n4["ReactivationService.__init__ (backend/app/services/task_reactivation_service.py)"]
    n5["test_cancel_and_reopen_keep_the_open_postponement (backend/tests/test_task_postponement.py)"]
    n6["test_deferred_and_postponed_are_independent (backend/tests/test_task_postponement.py)"]
    n7["test_only_a_pm_project_manager_or_operator_decides (backend/tests/test_task_postponement.py)"]
    n8["test_other_moves_into_or_out_of_postponed_are_refused (backend/tests/test_task_postponement.py)"]
    n9["test_reactivation_returns_work_with_brief_progress_evidence_and_provenance_intact (backend/tests/test_task_postponement.py)"]
    n10["test_requirements_must_be_possible_and_not_already_met (backend/tests/test_task_postponement.py)"]
    n11["test_snapshot_restore_cannot_move_work_into_or_out_of_postponed (backend/tests/test_task_postponement.py)"]
    n12["test_summary_rolls_up_postponed_leaves (backend/tests/test_task_postponement.py)"]
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
    click n0 "../modules/task_postponement_service.md"
    click n1 "../modules/routers_task_domain.md"
    click n2 "../modules/routers_task_domain.md"
    click n3 "../modules/routers_task_domain.md"
    click n4 "../modules/task_reactivation_service.md"
    click n5 "../modules/test_task_postponement.md"
    click n6 "../modules/test_task_postponement.md"
    click n7 "../modules/test_task_postponement.md"
    click n8 "../modules/test_task_postponement.md"
    click n9 "../modules/test_task_postponement.md"
    click n10 "../modules/test_task_postponement.md"
    click n11 "../modules/test_task_postponement.md"
    click n12 "../modules/test_task_postponement.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [task_postponement_service](../modules/task_postponement_service.md) | 10 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `postpone_task` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `reactivate_task` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `task_postponement` | call | [routers_task_domain](../modules/routers_task_domain.md) | 1 |
| `ReactivationService.__init__` | call | [task_reactivation_service](../modules/task_reactivation_service.md) | 1 |
| `test_cancel_and_reopen_keep_the_open_postponement` | call | [test_task_postponement](../modules/test_task_postponement.md) | 3 |
| `test_deferred_and_postponed_are_independent` | call | [test_task_postponement](../modules/test_task_postponement.md) | 2 |
| `test_only_a_pm_project_manager_or_operator_decides` | call | [test_task_postponement](../modules/test_task_postponement.md) | 5 |
| `test_other_moves_into_or_out_of_postponed_are_refused` | call | [test_task_postponement](../modules/test_task_postponement.md) | 1 |
| `test_reactivation_returns_work_with_brief_progress_evidence_and_provenance_intact` | call | [test_task_postponement](../modules/test_task_postponement.md) | 1 |
| `test_requirements_must_be_possible_and_not_already_met` | call | [test_task_postponement](../modules/test_task_postponement.md) | 1 |
| `test_snapshot_restore_cannot_move_work_into_or_out_of_postponed` | call | [test_task_postponement](../modules/test_task_postponement.md) | 1 |
| `test_summary_rolls_up_postponed_leaves` | call | [test_task_postponement](../modules/test_task_postponement.md) | 1 |

> References: showing 12 of 16 logical references; 4 omitted by the 12-row generated summary limit.
