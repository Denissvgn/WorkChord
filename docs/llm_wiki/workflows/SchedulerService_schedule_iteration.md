# SchedulerService_schedule_iteration

**Entry point:** `scheduler_service.SchedulerService.schedule_iteration`
**Modules involved:** [commands](../modules/commands.md), [iteration_service](../modules/iteration_service.md), [recovery](../modules/recovery.md), [scheduler_service](../modules/scheduler_service.md), [schemas_gantt](../modules/schemas_gantt.md)

> Schedule an iteration, optionally leaving commit ownership to the caller.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `iteration_service.IterationService`
2. `commands.lock_iterations`
3. `schemas_gantt.ScheduleResult`
4. `recovery.TaskScheduleBaseline`
5. `commands.commit_or_flush`
6. `schemas_gantt.ScheduleResult`

## Touches

- [commands](../modules/commands.md)
- [iteration_service](../modules/iteration_service.md)
- [recovery](../modules/recovery.md)
- [scheduler_service](../modules/scheduler_service.md)
- [schemas_gantt](../modules/schemas_gantt.md)

## Behavior

This workflow starts at `scheduler_service.SchedulerService.schedule_iteration`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
