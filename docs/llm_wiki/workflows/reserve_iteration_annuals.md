# reserve_iteration_annuals

**Entry point:** `calendar_rules.reserve_iteration_annuals`
**Modules involved:** [calendar_rules](../modules/calendar_rules.md), [commands](../modules/commands.md), [execution_planning_window](../modules/execution_planning_window.md), [iteration_service](../modules/iteration_service.md)

> A selection edits planning rules only. Refuse replacing a rule an issued task might still use.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `iteration_service.IterationService`
2. `iteration_service.IterationService.get_by_id`
3. `iteration_service.IterationService.changed_calendar_selection`
4. `execution_planning_window.live_assignments`
5. `commands.PlanningConflict`
6. `execution_planning_window.live_assignments`
7. `commands.PlanningConflict`

## Touches

- [calendar_rules](../modules/calendar_rules.md)
- [commands](../modules/commands.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [iteration_service](../modules/iteration_service.md)

## Behavior

This workflow starts at `calendar_rules.reserve_iteration_annuals`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
