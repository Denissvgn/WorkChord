# TaskService_add_dependency

**Entry point:** `task_service.TaskService.add_dependency`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [models_task](../modules/models_task.md), [task_brief_service](../modules/task_brief_service.md), [task_service](../modules/task_service.md)

> Add a dependency to a task.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `models_task.TaskDependency`
3. `task_brief_service.clear_execution_evidence`
4. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [models_task](../modules/models_task.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `task_service.TaskService.add_dependency`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.

Actual dependency changes invalidate current progress and acceptance through general updates and individual add/remove commands. Immutable evidence history remains available, a command reserves one task version, and no-op dependency requests retain their current version. Locked graph relationships are loaded explicitly before applying a dependency update.
