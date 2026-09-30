# CapacityService_set_calendar

**Entry point:** `capacity_service.CapacityService.set_calendar`
**Modules involved:** [authority](../modules/authority.md), [capacity_service](../modules/capacity_service.md), [commands](../modules/commands.md), [models_capacity](../modules/models_capacity.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.lock_planning`
2. `commands.PlanningConflict`
3. `authority.internal_authority`
4. `commands.PlanningConflict`
5. `models_capacity.ProfileAvailability`

## Touches

- [authority](../modules/authority.md)
- [capacity_service](../modules/capacity_service.md)
- [commands](../modules/commands.md)
- [models_capacity](../modules/models_capacity.md)

## Behavior

This workflow starts at `capacity_service.CapacityService.set_calendar`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
