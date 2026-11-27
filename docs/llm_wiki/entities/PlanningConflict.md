# PlanningConflict

**Location:** `backend/app/commands.py:54`
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
    n2["ImportReviewRefused (backend/app/services/import_review_service.py)"]
    n3["ProvenanceConflict (backend/app/services/manual_provenance_service.py)"]
    n4["MissingCalendarYear (backend/app/services/scheduler_service.py)"]
    n5["TimeEntryVersionConflict (backend/app/services/time_entry_service.py)"]
    n6["lock_iterations (backend/app/commands.py)"]
    n7["lock_planning (backend/app/commands.py)"]
    n8["planning_input_reservation (backend/app/commands.py)"]
    n9["planning_conflict (backend/app/main.py)"]
    n10["backend/app/mcp_server.py"]
    n11["backend/app/services/agent_planning_service.py"]
    n12["is_unused_allocation (backend/app/services/allocation_removal.py)"]
    n13["reserve_iteration_annuals (backend/app/services/calendar_rules.py)"]
    n14["CalendarService.delete (backend/app/services/calendar_service.py)"]
    n15["CapacityAdjustmentService._change (backend/app/services/capacity_adjustments.py)"]
    n16["CapacityAdjustmentService._refuse_reducing_issued_work (backend/app/services/capacity_adjustments.py)"]
    n17["CapacityService.invalidate_profile (backend/app/services/capacity_service.py)"]
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
    n14 --> n0
    n15 --> n0
    n16 --> n0
    n17 --> n0
    click n0 "../modules/commands.md"
    click n2 "../modules/import_review_service.md"
    click n3 "../modules/manual_provenance_service.md"
    click n4 "../modules/scheduler_service.md"
    click n5 "../modules/time_entry_service.md"
    click n6 "../modules/commands.md"
    click n7 "../modules/commands.md"
    click n8 "../modules/commands.md"
    click n9 "../modules/app_main.md"
    click n10 "../modules/mcp_server.md"
    click n11 "../modules/agent_planning_service.md"
    click n12 "../modules/allocation_removal.md"
    click n13 "../modules/calendar_rules.md"
    click n14 "../modules/calendar_service.md"
    click n15 "../modules/capacity_adjustments.md"
    click n16 "../modules/capacity_adjustments.md"
    click n17 "../modules/capacity_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [commands](../modules/commands.md) | 2 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |
| Subclass | `ImportReviewRefused` | [import_review_service](../modules/import_review_service.md) |
| Subclass | `ProvenanceConflict` | [manual_provenance_service](../modules/manual_provenance_service.md) |
| Subclass | `MissingCalendarYear` | [scheduler_service](../modules/scheduler_service.md) |
| Subclass | `TimeEntryVersionConflict` | [time_entry_service](../modules/time_entry_service.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `lock_iterations` | call | [commands](../modules/commands.md) | 1 |
| `lock_planning` | call | [commands](../modules/commands.md) | 1 |
| `planning_input_reservation` | call | [commands](../modules/commands.md) | 4 |
| `planning_conflict` | type_reference | [app_main](../modules/app_main.md) | — |
| `mcp_server` | import | [mcp_server](../modules/mcp_server.md) | — |
| `agent_planning_service` | import | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `is_unused_allocation` | call | [allocation_removal](../modules/allocation_removal.md) | 1 |
| `reserve_iteration_annuals` | call | [calendar_rules](../modules/calendar_rules.md) | 2 |
| `CalendarService.delete` | call | [calendar_service](../modules/calendar_service.md) | 2 |
| `CapacityAdjustmentService._change` | call | [capacity_adjustments](../modules/capacity_adjustments.md) | 7 |
| `CapacityAdjustmentService._refuse_reducing_issued_work` | call | [capacity_adjustments](../modules/capacity_adjustments.md) | 1 |
| `CapacityService.invalidate_profile` | call | [capacity_service](../modules/capacity_service.md) | 2 |

> References: showing 12 of 93 logical references; 81 omitted by the 12-row generated summary limit.
