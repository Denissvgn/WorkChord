# batch_update_tasks

**Entry point:** `tasks.batch_update_tasks`
**Modules involved:** [commands](../modules/commands.md), [iteration_service](../modules/iteration_service.md), [schemas_task](../modules/schemas_task.md), [tasks](../modules/tasks.md)

> Batch update multiple tasks in a single iteration under transaction block.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `iteration_service.IterationService`
2. `commands.command_transaction`
3. `commands.lock_iterations`
4. `schemas_task.TaskBatchUpdateResponse`

## Touches

- [commands](../modules/commands.md)
- [iteration_service](../modules/iteration_service.md)
- [schemas_task](../modules/schemas_task.md)
- [tasks](../modules/tasks.md)

## Behavior

This workflow starts at `tasks.batch_update_tasks`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
