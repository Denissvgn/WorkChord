# iteration_date_move Module

**Path:** `backend/app/services/iteration_date_move.py`

## Description

Preview a proposed iteration period against each person's shared capacity.

The preview runs the real iteration update inside a rolled-back command, so it
refuses exactly what the update would refuse and observes the same revisions.
It then compares, for every person of the iteration team and every date of the
proposed period, the hours this iteration's rows would request with the hours
the person's other rows already book, in any project. Dated capacity
adjustments apply on their dates. Nothing is saved.

Bookings in iterations the caller cannot read are reported only as a total,
the same way shared person capacity reports private busy hours.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `internal_authority` |
| `app.commands` | `PlanningConflict`, `current_command`, `lock_planning`, `preview_command` |
| `app.models.iteration` | `Iteration` |
| `app.models.team_member` | `TeamMember` |
| `app.schemas.iteration` | `IterationDateMoveRequest` |
| `app.services.calendar_rules` | `AnnualCalendars` |
| `app.services.calendar_service` | `CalendarService` |
| `app.services.capacity_adjustments` | `load_dated_availability` |
| `app.services.capacity_service` | `CapacityService`, `CapacityService` |
| `app.services.iteration_service` | `IterationService` |
| `app.services.planning_input_context` | `PlanningInputUnavailable`, `affected_iteration_ids` |
| `collections` | `defaultdict` |
| `datetime` | `timedelta` |
| `sqlalchemy` | `select` |
| `sqlalchemy.orm` | `selectinload` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/iteration_date_move.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/iteration_date_move.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (2) |
| Outbound | `backend` (11) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 13 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [IterationDateMoveService](../entities/IterationDateMoveService.md) | 44 | — | Calculate shared capacity for a proposed iteration period, then roll everything back. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_days` | `(start, end)` | — | — |
| `_rounded` | `(value)` | — | — |
