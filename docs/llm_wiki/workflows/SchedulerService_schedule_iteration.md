# SchedulerService_schedule_iteration

**Entry point:** `scheduler_service.SchedulerService.schedule_iteration`
**Modules involved:** [capacity_service](../modules/capacity_service.md), [commands](../modules/commands.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [iteration_service](../modules/iteration_service.md), [recovery](../modules/recovery.md), [scheduler_service](../modules/scheduler_service.md), [schemas_gantt](../modules/schemas_gantt.md)

> Schedule an iteration, optionally leaving commit ownership to the caller.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.lock_planning`
2. `iteration_service.IterationService`
3. `commands.lock_iterations`
4. `schemas_gantt.ScheduleResult`
5. `capacity_service.CapacityService`
6. `commands.PlanningConflict`
7. `schemas_gantt.SchedulingDecision`
8. `schemas_gantt.SchedulingDecision`
9. `delivery_dependency_service.DeliveryDependencyService`
10. `schemas_gantt.SchedulingDecision`
11. `schemas_gantt.SchedulingDecision`
12. `commands.PlanningConflict`
13. `recovery.TaskScheduleBaseline`
14. `capacity_service.CapacityService`
15. `commands.PlanningConflict`
16. `commands.commit_or_flush`
17. `schemas_gantt.ScheduleResult`

## Touches

- [capacity_service](../modules/capacity_service.md)
- [commands](../modules/commands.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [iteration_service](../modules/iteration_service.md)
- [recovery](../modules/recovery.md)
- [scheduler_service](../modules/scheduler_service.md)
- [schemas_gantt](../modules/schemas_gantt.md)

## Behavior

This workflow starts at `scheduler_service.SchedulerService.schedule_iteration`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
