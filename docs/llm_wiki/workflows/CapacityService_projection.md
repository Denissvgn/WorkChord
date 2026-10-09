# CapacityService_projection

**Entry point:** `capacity_service.CapacityService.projection`
**Modules involved:** [authority](../modules/authority.md), [capacity_service](../modules/capacity_service.md), [commands](../modules/commands.md), [services_work_metrics](../modules/services_work_metrics.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.PlanningConflict`
2. `authority.internal_authority`
3. `services_work_metrics.included_work_ids`

## Touches

- [authority](../modules/authority.md)
- [capacity_service](../modules/capacity_service.md)
- [commands](../modules/commands.md)
- [services_work_metrics](../modules/services_work_metrics.md)

## Behavior

This workflow starts at `capacity_service.CapacityService.projection`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
