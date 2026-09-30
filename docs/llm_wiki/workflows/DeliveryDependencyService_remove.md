# DeliveryDependencyService_remove

**Entry point:** `delivery_dependency_service.DeliveryDependencyService.remove`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [task_brief_service](../modules/task_brief_service.md), [task_service](../modules/task_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.lock_planning`
2. `task_service.TaskService`
3. `authority.require_project`
4. `task_brief_service.clear_execution_evidence`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `delivery_dependency_service.DeliveryDependencyService.remove`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
