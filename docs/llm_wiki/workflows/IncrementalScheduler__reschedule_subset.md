# IncrementalScheduler__reschedule_subset

**Entry point:** `scheduler_service.IncrementalScheduler._reschedule_subset`
**Modules involved:** [commands](../modules/commands.md), [iteration_service](../modules/iteration_service.md), [scheduler_service](../modules/scheduler_service.md), [services_work_metrics](../modules/services_work_metrics.md)

> Reschedule only the affected tasks.

Loads the affected tasks, clears their dates, and uses the
existing parallel scheduler to reschedule them.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `iteration_service.IterationService`
2. `services_work_metrics.effective_work_flags`
3. `commands.commit_or_flush`

## Touches

- [commands](../modules/commands.md)
- [iteration_service](../modules/iteration_service.md)
- [scheduler_service](../modules/scheduler_service.md)
- [services_work_metrics](../modules/services_work_metrics.md)

## Behavior

This workflow starts at `scheduler_service.IncrementalScheduler._reschedule_subset`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
