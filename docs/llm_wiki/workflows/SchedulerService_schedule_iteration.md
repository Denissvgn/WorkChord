# SchedulerService_schedule_iteration

**Entry point:** `scheduler_service.SchedulerService.schedule_iteration`
**Modules involved:** [capacity_service](../modules/capacity_service.md), [commands](../modules/commands.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [iteration_service](../modules/iteration_service.md), [recovery](../modules/recovery.md), [scheduler_service](../modules/scheduler_service.md), [schemas_gantt](../modules/schemas_gantt.md), [services_work_metrics](../modules/services_work_metrics.md)

> Schedule an iteration, optionally leaving commit ownership to the caller.

``follow_date`` recalculates the plan around what really happened: planned
work is placed on or after that date, finished work frees its assignee from
that date, running work holds its assignee at least through it, and a task
the calculation cannot place keeps its dates. ``anchor_task_id`` names the
task that started on ``follow_date``; it takes its assignee's row from there.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.lock_planning`
2. `iteration_service.IterationService`
3. `commands.lock_iterations`
4. `iteration_service.IterationService.get_by_id`
5. `schemas_gantt.ScheduleResult`
6. `capacity_service.CapacityService.schedule_issues`
7. `capacity_service.CapacityService`
8. `commands.PlanningConflict`
9. `services_work_metrics.effective_work_flags`
10. `schemas_gantt.SchedulingDecision`
11. `schemas_gantt.SchedulingDecision`
12. `delivery_dependency_service.DeliveryDependencyService.ready`
13. `delivery_dependency_service.DeliveryDependencyService`
14. `schemas_gantt.SchedulingDecision`
15. `schemas_gantt.SchedulingDecision`
16. `commands.PlanningConflict`
17. `recovery.TaskScheduleBaseline`
18. `capacity_service.CapacityService.schedule_issues`
19. `capacity_service.CapacityService`
20. `commands.PlanningConflict`
21. `commands.commit_or_flush`
22. `schemas_gantt.SchedulingDecision`
23. `schemas_gantt.ScheduleResult`

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
