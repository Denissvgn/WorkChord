# TaskService_merge_tasks

**Entry point:** `task_service.TaskService.merge_tasks`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [models_task](../modules/models_task.md), [snapshot_service](../modules/snapshot_service.md), [task_service](../modules/task_service.md)

> Merge multiple leaf tasks under a new parent task.

- All tasks must exist and belong to the same iteration
- All tasks must have no children (leaf nodes only)
- Creates a new parent task and updates parent_id for all merged tasks
- Parent derives the lowest numeric priority from child tasks

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.lock_iterations`
2. `snapshot_service.SnapshotService`
3. `authority.require_project`
4. `models_task.Task`
5. `commands.commit_or_flush`
6. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [models_task](../modules/models_task.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `task_service.TaskService.merge_tasks`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
