# TaskService_create

**Entry point:** `task_service.TaskService.create`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [models_task](../modules/models_task.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [snapshot_service](../modules/snapshot_service.md), [task_service](../modules/task_service.md)

> Create a new task.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.lock_iterations`
2. `authority.require_project`
3. `snapshot_service.SnapshotService`
4. `models_task.Task`
5. `models_task.TaskDependency`
6. `outbound_webhook_service.emit_outbound_webhook_event`
7. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [models_task](../modules/models_task.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `task_service.TaskService.create`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
