# CapacityService

**Location:** `backend/app/services/capacity_service.py:27`
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
| `calendar_status` | *(async)* `(member)` | — | — |
| `absence_ranges` | *(async)* `(member)` | — | Never return these private ranges to a transport; expose only capacity totals. |
| `invalidate_profile` | *(async)* `(profile_id)` | — | Update private derived revisions without exposing or rewriting their planning content. |
| `detail` | *(async)* `(profile_id)` | — | — |
| `set_calendar` | *(async)* `(profile_id, calendar_id, expected_version)` | `@atomic_command` | — |
| `save_absence` | *(async)* `(profile_id, start, end, *, absence_id = None, expected_version = None, deleted = False)` | `@atomic_command` | — |
| `projection` | *(async)* `(profile_id, start, end)` | — | — |
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
    n6["SchedulerService._build_member_schedules (backend/app/services/scheduler_service.py)"]
    n7["SchedulerService.schedule_iteration (backend/app/services/scheduler_service.py)"]
    n8["TeamService.add_vacation (backend/app/services/team_service.py)"]
    n9["TeamService.calculate_capacity (backend/app/services/team_service.py)"]
    n10["TeamService.delete_vacation (backend/app/services/team_service.py)"]
    n11["TeamService.get_workload (backend/app/services/team_service.py)"]
    n12["TeamService.update_vacation (backend/app/services/team_service.py)"]
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
    click n6 "../modules/scheduler_service.md"
    click n7 "../modules/scheduler_service.md"
    click n8 "../modules/team_service.md"
    click n9 "../modules/team_service.md"
    click n10 "../modules/team_service.md"
    click n11 "../modules/team_service.md"
    click n12 "../modules/team_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [capacity_service](../modules/capacity_service.md) | 12 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_absence` | call | [routers_capacity](../modules/routers_capacity.md) | 1 |
| `get_availability` | call | [routers_capacity](../modules/routers_capacity.md) | 1 |
| `get_profile_capacity` | call | [routers_capacity](../modules/routers_capacity.md) | 1 |
| `set_availability` | call | [routers_capacity](../modules/routers_capacity.md) | 1 |
| `update_absence` | call | [routers_capacity](../modules/routers_capacity.md) | 1 |
| `SchedulerService._build_member_schedules` | call | [scheduler_service](../modules/scheduler_service.md) | 1 |
| `SchedulerService.schedule_iteration` | call | [scheduler_service](../modules/scheduler_service.md) | 2 |
| `TeamService.add_vacation` | call | [team_service](../modules/team_service.md) | 1 |
| `TeamService.calculate_capacity` | call | [team_service](../modules/team_service.md) | 1 |
| `TeamService.delete_vacation` | call | [team_service](../modules/team_service.md) | 1 |
| `TeamService.get_workload` | call | [team_service](../modules/team_service.md) | 1 |
| `TeamService.update_vacation` | call | [team_service](../modules/team_service.md) | 1 |

> References: showing 12 of 23 logical references; 11 omitted by the 12-row generated summary limit.
