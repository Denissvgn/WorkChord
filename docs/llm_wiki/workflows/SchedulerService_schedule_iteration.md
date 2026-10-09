# SchedulerService_schedule_iteration

**Entry point:** `scheduler_service.SchedulerService.schedule_iteration`
**Modules involved:** [capacity_service](../modules/capacity_service.md), [commands](../modules/commands.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [iteration_service](../modules/iteration_service.md), [recovery](../modules/recovery.md), [scheduler_service](../modules/scheduler_service.md), [schemas_gantt](../modules/schemas_gantt.md), [services_work_metrics](../modules/services_work_metrics.md)

> Schedule an iteration, optionally leaving commit ownership to the caller.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.lock_planning`
2. `iteration_service.IterationService`
3. `commands.lock_iterations`
4. `schemas_gantt.ScheduleResult`
5. `capacity_service.CapacityService`
6. `commands.PlanningConflict`
7. `services_work_metrics.effective_work_flags`
8. `schemas_gantt.SchedulingDecision`
9. `schemas_gantt.SchedulingDecision`
10. `delivery_dependency_service.DeliveryDependencyService`
11. `schemas_gantt.SchedulingDecision`
12. `schemas_gantt.SchedulingDecision`
13. `commands.PlanningConflict`
14. `recovery.TaskScheduleBaseline`
15. `capacity_service.CapacityService`
16. `commands.PlanningConflict`
17. `commands.commit_or_flush`
18. `schemas_gantt.ScheduleResult`

## Touches

- [capacity_service](../modules/capacity_service.md)
- [commands](../modules/commands.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [iteration_service](../modules/iteration_service.md)
- [recovery](../modules/recovery.md)
- [scheduler_service](../modules/scheduler_service.md)
- [schemas_gantt](../modules/schemas_gantt.md)
- [services_work_metrics](../modules/services_work_metrics.md)

## Behavior

This workflow starts at `scheduler_service.SchedulerService.schedule_iteration`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
