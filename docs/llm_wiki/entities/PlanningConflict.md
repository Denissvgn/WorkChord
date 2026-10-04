# PlanningConflict

**Location:** `backend/app/commands.py:41`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [commands](../modules/commands.md)

## Description

_Auto-generated from `PlanningConflict` in `backend/app/commands.py`._

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(code, message)` | — | — |
| `detail` | `()` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["PlanningConflict (backend/app/commands.py)"]
    n1["RuntimeError"]
    n2["lock_iterations (backend/app/commands.py)"]
    n3["lock_planning (backend/app/commands.py)"]
    n4["planning_conflict (backend/app/main.py)"]
    n5["CalendarService.delete (backend/app/services/calendar_service.py)"]
    n6["CapacityService.projection (backend/app/services/capacity_service.py)"]
    n7["CapacityService.require_visible (backend/app/services/capacity_service.py)"]
    n8["CapacityService.save_absence (backend/app/services/capacity_service.py)"]
    n9["CapacityService.set_calendar (backend/app/services/capacity_service.py)"]
    n10["DeliveryDependencyService.add (backend/app/services/delivery_dependency_service.py)"]
    n11["DeliveryDependencyService.reconcile (backend/app/services/delivery_dependency_service.py)"]
    n12["DeliveryDependencyService.require_unreferenced (backend/app/services/delivery_dependency_service.py)"]
    n13["DeliveryDependencyService.validate_cycles (backend/app/services/delivery_dependency_service.py)"]
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
    n13 --> n0
    click n0 "../modules/commands.md"
    click n2 "../modules/commands.md"
    click n3 "../modules/commands.md"
    click n4 "../modules/app_main.md"
    click n5 "../modules/calendar_service.md"
    click n6 "../modules/capacity_service.md"
    click n7 "../modules/capacity_service.md"
    click n8 "../modules/capacity_service.md"
    click n9 "../modules/capacity_service.md"
    click n10 "../modules/delivery_dependency_service.md"
    click n11 "../modules/delivery_dependency_service.md"
    click n12 "../modules/delivery_dependency_service.md"
    click n13 "../modules/delivery_dependency_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [commands](../modules/commands.md) | 2 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `lock_iterations` | call | [commands](../modules/commands.md) | 1 |
| `lock_planning` | call | [commands](../modules/commands.md) | 1 |
| `planning_conflict` | type_reference | [app_main](../modules/app_main.md) | — |
| `CalendarService.delete` | call | [calendar_service](../modules/calendar_service.md) | 1 |
| `CapacityService.projection` | call | [capacity_service](../modules/capacity_service.md) | 1 |
| `CapacityService.require_visible` | call | [capacity_service](../modules/capacity_service.md) | 1 |
| `CapacityService.save_absence` | call | [capacity_service](../modules/capacity_service.md) | 3 |
| `CapacityService.set_calendar` | call | [capacity_service](../modules/capacity_service.md) | 2 |
| `DeliveryDependencyService.add` | call | [delivery_dependency_service](../modules/delivery_dependency_service.md) | 1 |
| `DeliveryDependencyService.reconcile` | call | [delivery_dependency_service](../modules/delivery_dependency_service.md) | 1 |
| `DeliveryDependencyService.require_unreferenced` | call | [delivery_dependency_service](../modules/delivery_dependency_service.md) | 1 |
| `DeliveryDependencyService.validate_cycles` | call | [delivery_dependency_service](../modules/delivery_dependency_service.md) | 1 |

> References: showing 12 of 23 logical references; 11 omitted by the 12-row generated summary limit.
