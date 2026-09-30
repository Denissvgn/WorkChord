# TaskService_create

**Entry point:** `task_service.TaskService.create`
**Modules involved:** [authority](../modules/authority.md), [backlog_snapshot_service](../modules/backlog_snapshot_service.md), [commands](../modules/commands.md), [models_task](../modules/models_task.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [snapshot_service](../modules/snapshot_service.md), [task_brief_service](../modules/task_brief_service.md), [task_domain_service](../modules/task_domain_service.md), [task_service](../modules/task_service.md)

> Create a new task.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.lock_iterations`
2. `commands.lock_backlog_project`
3. `backlog_snapshot_service.BacklogSnapshotService`
4. `authority.require_project`
5. `task_domain_service.nominal_day_hours`
6. `task_domain_service.normalize_effort`
7. `task_domain_service.require_owner`
8. `snapshot_service.SnapshotService`
9. `models_task.Task`
10. `task_brief_service.TaskBriefService`
11. `models_task.TaskDependency`
12. `outbound_webhook_service.emit_outbound_webhook_event`
13. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [backlog_snapshot_service](../modules/backlog_snapshot_service.md)
- [commands](../modules/commands.md)
- [models_task](../modules/models_task.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_domain_service](../modules/task_domain_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `task_service.TaskService.create`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
