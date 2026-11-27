# PlanningState

**Location:** `backend/app/models/capacity.py:12`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_capacity](../modules/models_capacity.md)

## Description

Lazy singleton used to serialize shared planning before iteration and task reservations. Each command reserves one revision; preview and failure roll back that reservation with domain changes. This is a coarse workspace serialization boundary, not a global scheduling optimizer.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True)` | — |
| `revision` | `Mapped[int]` | `mapped_column(Integer, nullable=False, default=0)` | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["PlanningState (backend/app/models/capacity.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/commands.py"]
    n3["backend/app/models/__init__.py"]
    n4["backend/app/services/allocation_removal.py"]
    n5["backend/app/services/capacity_service.py"]
    n6["backend/tests/test_capacity_adjustments.py"]
    n7["backend/tests/test_iteration_date_move.py"]
    n8["backend/tests/test_profile_capacity.py"]
    n9["backend/tests/test_task_discussion.py"]
    n10["backend/tests/test_task_reactivation.py"]
    n11["backend/tests/test_team_pm_recovery.py"]
    n12["backend/tests/test_unused_allocation.py"]
    n0 --> n1
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
    click n0 "../modules/models_capacity.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/commands.md"
    click n3 "../modules/models___init__.md"
    click n4 "../modules/allocation_removal.md"
    click n5 "../modules/capacity_service.md"
    click n6 "../modules/test_capacity_adjustments.md"
    click n7 "../modules/test_iteration_date_move.md"
    click n8 "../modules/test_profile_capacity.md"
    click n9 "../modules/test_task_discussion.md"
    click n10 "../modules/test_task_reactivation.md"
    click n11 "../modules/test_team_pm_recovery.md"
    click n12 "../modules/test_unused_allocation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_capacity](../modules/models_capacity.md) | 0 | `id`, `revision` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `commands` | import | [commands](../modules/commands.md) | — |
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `allocation_removal` | import | [allocation_removal](../modules/allocation_removal.md) | — |
| `capacity_service` | import | [capacity_service](../modules/capacity_service.md) | — |
| `test_capacity_adjustments` | import | [test_capacity_adjustments](../modules/test_capacity_adjustments.md) | — |
| `test_iteration_date_move` | import | [test_iteration_date_move](../modules/test_iteration_date_move.md) | — |
| `test_profile_capacity` | import | [test_profile_capacity](../modules/test_profile_capacity.md) | — |
| `test_task_discussion` | import | [test_task_discussion](../modules/test_task_discussion.md) | — |
| `test_task_reactivation` | import | [test_task_reactivation](../modules/test_task_reactivation.md) | — |
| `test_team_pm_recovery` | import | [test_team_pm_recovery](../modules/test_team_pm_recovery.md) | — |
| `test_unused_allocation` | import | [test_unused_allocation](../modules/test_unused_allocation.md) | — |
