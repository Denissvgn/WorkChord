# TaskService_move_task

**Entry point:** `task_service.TaskService.move_task`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [snapshot_service](../modules/snapshot_service.md), [task_domain_service](../modules/task_domain_service.md), [task_service](../modules/task_service.md)

> Move a task subtree to an iteration, applying scoped project inheritance.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `task_domain_service.require_owner`
2. `authority.require_project`
3. `authority.require_project`
4. `snapshot_service.SnapshotService`
5. `task_domain_service.nominal_day_hours`
6. `outbound_webhook_service.emit_outbound_webhook_event`
7. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_domain_service](../modules/task_domain_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `task_service.TaskService.move_task`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
