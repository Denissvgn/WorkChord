# ProjectService_delete

**Entry point:** `project_service.ProjectService.delete`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [project_service](../modules/project_service.md)

> Delete a project, optionally detaching linked tasks first.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `commands.lock_planning`
3. `authority.internal_authority`
4. `commands.PlanningConflict`
5. `delivery_dependency_service.DeliveryDependencyService.require_unreferenced`
6. `delivery_dependency_service.DeliveryDependencyService`
7. `authority.internal_authority`
8. `commands.PlanningConflict`
9. `delivery_dependency_service.DeliveryDependencyService.require_unreferenced`
10. `delivery_dependency_service.DeliveryDependencyService`
11. `outbound_webhook_service.emit_outbound_webhook_event`
12. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [project_service](../modules/project_service.md)

## Behavior

This workflow starts at `project_service.ProjectService.delete`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
