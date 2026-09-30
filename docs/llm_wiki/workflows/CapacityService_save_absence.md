# CapacityService_save_absence

**Entry point:** `capacity_service.CapacityService.save_absence`
**Modules involved:** [authority](../modules/authority.md), [capacity_service](../modules/capacity_service.md), [commands](../modules/commands.md), [models_capacity](../modules/models_capacity.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.PlanningConflict`
2. `commands.lock_planning`
3. `authority.internal_authority`
4. `commands.PlanningConflict`
5. `commands.PlanningConflict`
6. `models_capacity.ProfileAbsence`

## Touches

- [authority](../modules/authority.md)
- [capacity_service](../modules/capacity_service.md)
- [commands](../modules/commands.md)
- [models_capacity](../modules/models_capacity.md)

## Behavior

This workflow starts at `capacity_service.CapacityService.save_absence`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
