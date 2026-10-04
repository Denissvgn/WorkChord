# TaskService_remove_dependency

**Entry point:** `task_service.TaskService.remove_dependency`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [task_brief_service](../modules/task_brief_service.md), [task_service](../modules/task_service.md)

> Remove a dependency from a task.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `task_brief_service.clear_execution_evidence`
3. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `task_service.TaskService.remove_dependency`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
