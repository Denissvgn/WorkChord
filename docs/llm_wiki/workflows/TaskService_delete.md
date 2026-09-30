# TaskService_delete

**Entry point:** `task_service.TaskService.delete`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [external_link_service](../modules/external_link_service.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [snapshot_service](../modules/snapshot_service.md), [task_service](../modules/task_service.md)

> Delete a task and its subtasks.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `delivery_dependency_service.DeliveryDependencyService`
3. `snapshot_service.SnapshotService`
4. `authority.internal_authority`
5. `external_link_service.ExternalLinkService`
6. `outbound_webhook_service.emit_outbound_webhook_event`
7. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [external_link_service](../modules/external_link_service.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `task_service.TaskService.delete`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
