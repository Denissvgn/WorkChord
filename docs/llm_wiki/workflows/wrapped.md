# wrapped

**Entry point:** `commands.wrapped`
**Modules involved:** [commands](../modules/commands.md), [planning_input_context](../modules/planning_input_context.md), [snapshot_service](../modules/snapshot_service.md), [task_service](../modules/task_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `planning_input_context.affected_iteration_ids`
2. `snapshot_service.SnapshotService`
3. `task_service.TaskService`

## Touches

- [commands](../modules/commands.md)
- [planning_input_context](../modules/planning_input_context.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `commands.wrapped`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
