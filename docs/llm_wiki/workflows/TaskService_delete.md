# TaskService_delete

**Entry point:** `task_service.TaskService.delete`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [external_link_service](../modules/external_link_service.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [snapshot_service](../modules/snapshot_service.md), [task_postponement_service](../modules/task_postponement_service.md), [task_service](../modules/task_service.md)

> Delete a task and its subtasks.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `delivery_dependency_service.DeliveryDependencyService.require_unreferenced`
3. `delivery_dependency_service.DeliveryDependencyService`
4. `task_postponement_service.require_unreferenced`
5. `snapshot_service.SnapshotService`
6. `authority.internal_authority`
7. `external_link_service.ExternalLinkService.delete_for_entity`
8. `external_link_service.ExternalLinkService`
9. `outbound_webhook_service.emit_outbound_webhook_event`
10. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [external_link_service](../modules/external_link_service.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_postponement_service](../modules/task_postponement_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `task_service.TaskService.delete`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
