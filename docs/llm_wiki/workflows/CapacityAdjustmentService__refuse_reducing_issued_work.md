# CapacityAdjustmentService__refuse_reducing_issued_work

**Entry point:** `capacity_adjustments.CapacityAdjustmentService._refuse_reducing_issued_work`
**Modules involved:** [authority](../modules/authority.md), [calendar_rules](../modules/calendar_rules.md), [capacity_adjustments](../modules/capacity_adjustments.md), [commands](../modules/commands.md), [execution_planning_window](../modules/execution_planning_window.md)

> A reduction must not change the capacity that this row's issued work was planned with.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.internal_authority`
2. `execution_planning_window.live_assignments`
3. `commands.PlanningConflict`
4. `calendar_rules.issued_coordinates`

## Touches

- [authority](../modules/authority.md)
- [calendar_rules](../modules/calendar_rules.md)
- [capacity_adjustments](../modules/capacity_adjustments.md)
- [commands](../modules/commands.md)
- [execution_planning_window](../modules/execution_planning_window.md)

## Behavior

Refuses a reduction that would change the capacity a row's issued work was planned with, naming the affected task and assignment IDs so they can be finished or reconciled first, or other dates reduced instead.
