# CapacityService

**Location:** `backend/app/services/capacity_service.py:126`
**Kind:** Class
**Bases:** —
**Module:** [capacity_service](../modules/capacity_service.md)

## Description

Owns person availability commands and date-bounded cross-project capacity projections. The linked human or an operator may edit the calendar and versioned absences. Private allocations contribute only aggregate busy hours; unestimated commitments remain explicitly unknown.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(db)` | — | — |
| `require_owner` | `(profile_id)` | — | — |
| `require_visible` | *(async)* `(profile_id)` | — | — |
| `calendar_for` | *(async)* `(member)` | — | Use durable rules; retain a flagged local fallback until conflicts are reconciled. |
| `coverage_for` | *(async)* `(member)` | — | A profile owner's selection is authoritative; otherwise use this iteration's rules. |
| `calendar_status` | *(async)* `(member)` | — | — |
| `absence_ranges` | *(async)* `(member)` | — | Never return these private ranges to a transport; expose only capacity totals. |
| `invalidate_profile` | *(async)* `(profile_id, *, annual_selection = None, annual_only = False)` | — | Update private derived revisions without exposing or rewriting their planning content. |
| `detail` | *(async)* `(profile_id)` | — | — |
| `set_calendar` | *(async)* `(profile_id, calendar_id, expected_version, additional_calendar_ids = None)` | `@atomic_command` | — |
| `save_absence` | *(async)* `(profile_id, start, end, *, absence_id = None, expected_version = None, deleted = False)` | `@atomic_command` | — |
| `projection` | *(async)* `(profile_id, start, end)` | — | — |
| `_projection` | *(async)* `(profile_id, start, end)` | — | — |
| `schedule_issues` | *(async)* `(iteration, members)` | — | Return aggregate constraints without exposing private work or changing existing plans. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CapacityService (backend/app/services/capacity_service.py)"]
    n1["create_absence (backend/app/routers/capacity.py)"]
    n2["get_availability (backend/app/routers/capacity.py)"]
    n3["get_profile_capacity (backend/app/routers/capacity.py)"]
    n4["set_availability (backend/app/routers/capacity.py)"]
    n5["update_absence (backend/app/routers/capacity.py)"]
    n6["AgentPlanningService._schedule_input_digest (backend/app/services/agent_planning_service.py)"]
    n7["AgentRoutingService._capacity_inputs (backend/app/services/agent_routing_service.py)"]
    n8["CapacityAdjustmentService._change (backend/app/services/capacity_adjustments.py)"]
    n9["CapacityAdjustmentService._projection (backend/app/services/capacity_adjustments.py)"]
    n10["CapacityTransferService._row_hours (backend/app/services/capacity_transfers.py)"]
    n11["IterationDateMoveService._row_hours (backend/app/services/iteration_date_move.py)"]
    n12["IterationDateMoveService.preview (backend/app/services/iteration_date_move.py)"]
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
    click n0 "../modules/capacity_service.md"
    click n1 "../modules/routers_capacity.md"
    click n2 "../modules/routers_capacity.md"
    click n3 "../modules/routers_capacity.md"
    click n4 "../modules/routers_capacity.md"
    click n5 "../modules/routers_capacity.md"
    click n6 "../modules/agent_planning_service.md"
    click n7 "../modules/agent_routing_service.md"
    click n8 "../modules/capacity_adjustments.md"
    click n9 "../modules/capacity_adjustments.md"
    click n10 "../modules/capacity_transfers.md"
    click n11 "../modules/iteration_date_move.md"
    click n12 "../modules/iteration_date_move.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [capacity_service](../modules/capacity_service.md) | 14 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_absence` | call | [routers_capacity](../modules/routers_capacity.md) | 1 |
| `get_availability` | call | [routers_capacity](../modules/routers_capacity.md) | 1 |
| `get_profile_capacity` | call | [routers_capacity](../modules/routers_capacity.md) | 1 |
| `set_availability` | call | [routers_capacity](../modules/routers_capacity.md) | 1 |
| `update_absence` | call | [routers_capacity](../modules/routers_capacity.md) | 1 |
| `AgentPlanningService._schedule_input_digest` | call | [agent_planning_service](../modules/agent_planning_service.md) | 1 |
| `AgentRoutingService._capacity_inputs` | call | [agent_routing_service](../modules/agent_routing_service.md) | 1 |
| `CapacityAdjustmentService._change` | call | [capacity_adjustments](../modules/capacity_adjustments.md) | 1 |
| `CapacityAdjustmentService._projection` | call | [capacity_adjustments](../modules/capacity_adjustments.md) | 1 |
| `CapacityTransferService._row_hours` | call | [capacity_transfers](../modules/capacity_transfers.md) | 1 |
| `IterationDateMoveService._row_hours` | call | [iteration_date_move](../modules/iteration_date_move.md) | 1 |
| `IterationDateMoveService.preview` | call | [iteration_date_move](../modules/iteration_date_move.md) | 1 |

> References: showing 12 of 39 logical references; 27 omitted by the 12-row generated summary limit.
