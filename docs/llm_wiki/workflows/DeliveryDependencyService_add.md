# DeliveryDependencyService_add

**Entry point:** `delivery_dependency_service.DeliveryDependencyService.add`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [delivery_dependency](../modules/delivery_dependency.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [task_brief_service](../modules/task_brief_service.md), [task_service](../modules/task_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.PlanningConflict`
2. `commands.lock_planning`
3. `task_service.TaskService`
4. `authority.require_project`
5. `authority.require_project`
6. `delivery_dependency.DeliveryDependency`
7. `task_brief_service.clear_execution_evidence`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [delivery_dependency](../modules/delivery_dependency.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_service](../modules/task_service.md)

## Behavior

Requires edit permission on the dependent task, read permission on the target and the supplied task version. It locks shared planning before graph mutation, validates task/milestone cycles and clears stale current evidence while retaining history. Any failure rolls back the complete command.
