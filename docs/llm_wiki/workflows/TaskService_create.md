# TaskService_create

**Entry point:** `task_service.TaskService.create`
**Modules involved:** [models_task](../modules/models_task.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [snapshot_service](../modules/snapshot_service.md), [task_service](../modules/task_service.md)

> Create a new task.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `snapshot_service.SnapshotService`
2. `models_task.Task`
3. `models_task.TaskDependency`
4. `outbound_webhook_service.emit_outbound_webhook_event`

## Touches

- [models_task](../modules/models_task.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `task_service.TaskService.create`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
