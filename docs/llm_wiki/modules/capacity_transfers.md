# capacity_transfers Module

**Path:** `backend/app/services/capacity_transfers.py`

## Description

Temporary capacity transfers between rows of one person, with a dated return.

A transfer lends part of the availability percentage of one or more source rows
(each an iteration's capacity row, usually in different projects) to a target row
of the same person for a bounded date range. It is recorded as dated adjustments,
one per row, that share one group token: each source counts its own percentage
minus the lent percentage and the target its own percentage plus the sum of the
lent percentages, on the transfer's dates only. Every other date keeps each row's
own percentage, so the prior shares apply again after the end date without any
scheduled job, and the rows' own percentages are never edited.

Recording or withdrawing a transfer is one shared planning input command over the
planning scope of every row it changes, so both sides change together or not at
all and an intervening change to any affected iteration is a revision conflict. It
changes no task, assignment or run. A source reduction on dates where that row's
issued work is scheduled is refused, as is restoring the target on such dates.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `internal_authority` |
| `app.commands` | `PlanningConflict`, `current_command`, `planning_input_reservation`, `preview_command`, `schedule_input_command` |
| `app.models.calendar` | `Calendar` |
| `app.models.identity` | `CommandAudit` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.team_member` | `TeamMember`, `TeamMemberCapacityAdjustment` |
| `app.services.capacity_adjustments` | `MAX_ACTIVE_ADJUSTMENTS`, `CapacityAdjustmentService`, `_days`, `_response` |
| `app.services.capacity_service` | `CapacityService` |
| `app.services.planning_input_context` | `PlanningInputUnavailable`, `affected_iteration_ids` |
| `app.services.work_metrics` | `working_today` |
| `app.utils.time` | `utc_now` |
| `datetime` | `timedelta` |
| `sqlalchemy` | `func`, `select` |
| `sqlalchemy.orm` | `selectinload` |
| `uuid` | `uuid4` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/capacity_transfers.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/capacity_transfers.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (7) |
| Outbound | `backend` (12) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 17 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [_RowHours](../entities/RowHours.md) | 119 | — | Calendar hours of one row on each date, after the person's absences. |
| [CapacityTransferService](../entities/CapacityTransferService.md) | 131 | — | Preview, record, withdraw and read temporary capacity transfers. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_unavailable` | `(message = 'Capacity transfer not found or inaccessible')` | — | — |
| `transfer_group_members` | *(async)* `(db, group_token)` | — | Return the capacity rows of a recorded transfer, or None when the token names no transfer. |
| `transfer_member_ids` | *(async)* `(db, values)` | — | Resolve every row a transfer command changes, for its planning reservation. |
| `transfer_iteration_ids` | *(async)* `(db, values)` | — | The planning scope of a transfer is the union of the scopes of all of its rows. |
| `refuse_withdrawing_transfer_side` | *(async)* `(db, rows)` | — | A single-row command must not withdraw one side of a transfer and leave the other in place. |
| `refuse_removing_transfer_row` | *(async)* `(db, member_id)` | — | Removing a row would leave the other rows of an unfinished transfer changed alone. |
| `_round` | `(value)` | — | — |
