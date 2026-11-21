# CapacityService_set_calendar

**Entry point:** `capacity_service.CapacityService.set_calendar`
**Modules involved:** [authority](../modules/authority.md), [calendar_rules](../modules/calendar_rules.md), [calendar_service](../modules/calendar_service.md), [capacity_service](../modules/capacity_service.md), [commands](../modules/commands.md), [models_capacity](../modules/models_capacity.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.lock_planning`
2. `commands.PlanningConflict`
3. `calendar_service.CalendarService.selected_years`
4. `calendar_service.CalendarService`
5. `commands.PlanningConflict`
6. `authority.internal_authority`
7. `commands.PlanningConflict`
8. `calendar_rules.AnnualCalendars`
9. `commands.PlanningConflict`
10. `calendar_rules.AnnualCalendars`
11. `models_capacity.ProfileAvailability`

## Touches

- [authority](../modules/authority.md)
- [calendar_rules](../modules/calendar_rules.md)
- [calendar_service](../modules/calendar_service.md)
- [capacity_service](../modules/capacity_service.md)
- [commands](../modules/commands.md)
- [models_capacity](../modules/models_capacity.md)

## Behavior

This workflow starts at `capacity_service.CapacityService.set_calendar`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
