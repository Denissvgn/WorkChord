# DeliveryDependencyService_retarget

**Entry point:** `delivery_dependency_service.DeliveryDependencyService.retarget`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [task_service](../modules/task_service.md)

> Change or clear the branch on which a prerequisite's accepted code must be merged.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.lock_planning`
2. `task_service.TaskService`
3. `task_service.TaskService.get_by_id`
4. `authority.require_project`
5. `authority.require_project`
6. `task_service.TaskService.ensure_expected_version`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [task_service](../modules/task_service.md)

## Behavior

Locks planning, loads the task and requires project edit access, then finds the edge on that task and reads its prerequisite with read access. The branch is normalized (a `refs/heads/` prefix is dropped; no spaces, at most 255 characters) and only a task prerequisite may carry one, and never a summary task. The expected task version is checked, and a changed branch is applied only after the task version is reserved and the task is confirmed to have no claimed structure. Applying it clears execution evidence, records a `delivery_prerequisite_retargeted` task event with the previous and new branch, and marks the task as a changed delivery node so dependents are re-evaluated. Setting the branch the edge already has changes nothing. A null branch keeps only the acceptance gate. It returns the refreshed projection.
