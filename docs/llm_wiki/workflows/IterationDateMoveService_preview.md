# IterationDateMoveService_preview

**Entry point:** `iteration_date_move.IterationDateMoveService.preview`
**Modules involved:** [authority](../modules/authority.md), [capacity_service](../modules/capacity_service.md), [commands](../modules/commands.md), [iteration_date_move](../modules/iteration_date_move.md), [iteration_service](../modules/iteration_service.md), [planning_input_context](../modules/planning_input_context.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `iteration_service.IterationService`
2. `iteration_service.IterationService.get_by_id`
3. `planning_input_context.PlanningInputUnavailable`
4. `planning_input_context.affected_iteration_ids`
5. `commands.PlanningConflict`
6. `commands.PlanningConflict`
7. `commands.lock_planning`
8. `authority.internal_authority`
9. `commands.PlanningConflict`
10. `capacity_service.CapacityService`
11. `capacity_service.CapacityService._projection`
12. `planning_input_context.PlanningInputUnavailable`
13. `commands.current_command`
14. `capacity_service.CapacityService._projection`

## Touches

- [authority](../modules/authority.md)
- [capacity_service](../modules/capacity_service.md)
- [commands](../modules/commands.md)
- [iteration_date_move](../modules/iteration_date_move.md)
- [iteration_service](../modules/iteration_service.md)
- [planning_input_context](../modules/planning_input_context.md)

## Behavior

Previews a proposed iteration period against each person's shared capacity. It runs the real iteration update inside a rolled-back command, so it refuses exactly what the update would refuse and observes the same revisions, then compares, per person of the iteration team and per date of the proposed period, the hours this iteration's rows would request with the hours the person's other rows already book in any project, with dated adjustments applied. Bookings in iterations the caller cannot read are reported only as a total. Nothing is saved.
