# IterationDateMoveService__row_hours

**Entry point:** `iteration_date_move.IterationDateMoveService._row_hours`
**Modules involved:** [authority](../modules/authority.md), [capacity_adjustments](../modules/capacity_adjustments.md), [capacity_service](../modules/capacity_service.md), [iteration_date_move](../modules/iteration_date_move.md)

> Return a function giving this iteration's and the other rows' hours of one person on a date.

Uses the same inputs as the shared person capacity: the person's calendar,
or each row's iteration calendar, minus absences, times the row's
percentage on that date.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `capacity_service.CapacityService`
2. `authority.internal_authority`
3. `capacity_service.CapacityService.coverage_for`
4. `capacity_service.CapacityService.absence_ranges`
5. `capacity_adjustments.load_dated_availability`

## Touches

- [authority](../modules/authority.md)
- [capacity_adjustments](../modules/capacity_adjustments.md)
- [capacity_service](../modules/capacity_service.md)
- [iteration_date_move](../modules/iteration_date_move.md)

## Behavior

Returns each person's hours on a date for this iteration's rows and for the other rows, from the person's calendar or each row's iteration calendar minus absences, times the row's dated percentage; the same inputs as shared person capacity.
