# preview_iteration_schedule

**Entry point:** `gantt.preview_iteration_schedule`
**Modules involved:** [commands](../modules/commands.md), [iteration_service](../modules/iteration_service.md), [routers_gantt](../modules/routers_gantt.md), [schemas_gantt](../modules/schemas_gantt.md), [task_service](../modules/task_service.md), [tasks](../modules/tasks.md)

> Dry-run sandbox edits through the real scheduler and roll everything back.

Applies the submitted task changes (same item shape as batch-update) and
runs the actual scheduling pass in one transaction, serializes the
projected Gantt state, then rolls the transaction back. The preview is
therefore always consistent with what a subsequent batch-update apply
(which auto-reschedules) will produce.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `iteration_service.IterationService`
2. `task_service.TaskService`
3. `commands.command_transaction`
4. `commands.lock_iterations`
5. `tasks.apply_batch_update_items`
6. `schemas_gantt.SchedulePreviewResponse`

## Touches

- [commands](../modules/commands.md)
- [iteration_service](../modules/iteration_service.md)
- [routers_gantt](../modules/routers_gantt.md)
- [schemas_gantt](../modules/schemas_gantt.md)
- [task_service](../modules/task_service.md)
- [tasks](../modules/tasks.md)

## Behavior

This workflow starts at `gantt.preview_iteration_schedule`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
