# PlanningInputUnavailable

**Location:** `backend/app/services/planning_input_context.py:10`
**Kind:** Class
**Bases:** `LookupError`
**Module:** [planning_input_context](../modules/planning_input_context.md)

## Description

A shared planning input is absent or outside the authorized graph.

## Attributes

*No annotated attributes found.*

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["PlanningInputUnavailable (backend/app/services/planning_input_context.py)"]
    n1["LookupError"]
    n2["planning_input_unavailable_handler (backend/app/main.py)"]
    n3["CapacityAdjustmentService._member (backend/app/services/capacity_adjustments.py)"]
    n4["_unavailable (backend/app/services/capacity_transfers.py)"]
    n5["IterationDateMoveService.preview (backend/app/services/iteration_date_move.py)"]
    n6["affected_iteration_ids (backend/app/services/planning_input_context.py)"]
    n7["observe_planning_input (backend/app/services/planning_input_context.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/planning_input_context.md"
    click n2 "../modules/app_main.md"
    click n3 "../modules/capacity_adjustments.md"
    click n4 "../modules/capacity_transfers.md"
    click n5 "../modules/iteration_date_move.md"
    click n6 "../modules/planning_input_context.md"
    click n7 "../modules/planning_input_context.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [planning_input_context](../modules/planning_input_context.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `LookupError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `planning_input_unavailable_handler` | type_reference | [app_main](../modules/app_main.md) | — |
| `CapacityAdjustmentService._member` | call | [capacity_adjustments](../modules/capacity_adjustments.md) | 1 |
| `_unavailable` | call | [capacity_transfers](../modules/capacity_transfers.md) | 1 |
| `IterationDateMoveService.preview` | call | [iteration_date_move](../modules/iteration_date_move.md) | 2 |
| `affected_iteration_ids` | call | [planning_input_context](../modules/planning_input_context.md) | 1 |
| `observe_planning_input` | call | [planning_input_context](../modules/planning_input_context.md) | 1 |
