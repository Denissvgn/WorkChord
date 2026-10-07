# capacity_service Module

**Path:** `backend/app/services/capacity_service.py`

## Description

Owns versioned person calendar and absence commands, date-based capacity projections, and commitment constraints. Managed edits require the linked human or an operator; trusted-local mode retains its explicit open boundary. Absence unions, calendar hours, allocation, utilization and coefficients are applied once. Private allocations contribute aggregate busy time only. Unknown effort and calendar coverage remain explicit; commitments require linked profiles, sufficient capacity and allocation date coverage.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `AuthorityError`, `internal_authority` |
| `app.commands` | `PlanningConflict`, `atomic_command`, `lock_iterations`, `lock_planning` |
| `app.models.calendar` | `Calendar` |
| `app.models.capacity` | `PlanningState`, `ProfileAbsence`, `ProfileAvailability` |
| `app.models.iteration` | `Iteration` |
| `app.models.team_member` | `TeamMember`, `TeamMemberProfile`, `Vacation` |
| `datetime` | `date`, `timedelta` |
| `sqlalchemy` | `delete`, `select`, `update` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/authority.py"]
    n1["backend/app/commands.py"]
    n2["backend/app/models/calendar.py"]
    n3["backend/app/models/capacity.py"]
    n4["backend/app/models/iteration.py"]
    n5["backend/app/models/team_member.py"]
    n6["backend/app/routers/capacity.py"]
    n7["backend/app/services/capacity_service.py"]
    n8["backend/tests/test_profile_capacity.py"]
    n9["scripts/load/service_worksets.py"]
    n1 --> n0
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n2 --> n4
    n4 --> n2
    n4 --> n5
    n5 --> n4
    n6 --> n7
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n4
    n7 --> n5
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n8 --> n3
    n8 --> n4
    n8 --> n5
    n8 --> n7
    n9 --> n0
    n9 --> n4
    n9 --> n7
    click n0 "../modules/authority.md"
    click n1 "../modules/commands.md"
    click n2 "../modules/models_calendar.md"
    click n3 "../modules/models_capacity.md"
    click n4 "../modules/models_iteration.md"
    click n5 "../modules/team_member.md"
    click n6 "../modules/routers_capacity.md"
    click n7 "../modules/capacity_service.md"
    click n8 "../modules/test_profile_capacity.md"
    click n9 "../modules/service_worksets.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [routers_capacity](../modules/routers_capacity.md) |
| Inbound | [test_profile_capacity](../modules/test_profile_capacity.md) |
| Inbound | [service_worksets](../modules/service_worksets.md) |
| Outbound | [authority](../modules/authority.md) |
| Outbound | [commands](../modules/commands.md) |
| Outbound | [models_calendar](../modules/models_calendar.md) |
| Outbound | [models_capacity](../modules/models_capacity.md) |
| Outbound | [models_iteration](../modules/models_iteration.md) |
| Outbound | [team_member](../modules/team_member.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [CapacityService](../entities/CapacityService.md) | 27 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `day_hours` | `(calendar, day)` | — | Nominal local-date hours, with each holiday/weekend/short-day rule applied once. |
| `calendar_signature` | `(calendar)` | — | — |