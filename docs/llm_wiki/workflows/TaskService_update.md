# TaskService_update

**Entry point:** `task_service.TaskService.update`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [models_task](../modules/models_task.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [snapshot_service](../modules/snapshot_service.md), [task_service](../modules/task_service.md)

> Update an existing task.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `snapshot_service.SnapshotService`
3. `models_task.TaskDependency`
4. `outbound_webhook_service.emit_outbound_webhook_event`
5. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [models_task](../modules/models_task.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `task_service.TaskService.update`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
