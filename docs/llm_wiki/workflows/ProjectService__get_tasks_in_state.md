# ProjectService__get_tasks_in_state

**Entry point:** `project_service.ProjectService._get_tasks_in_state`
**Modules involved:** [project_service](../modules/project_service.md), [query_limits](../modules/query_limits.md), [task_display_state](../modules/task_display_state.md), [task_service](../modules/task_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `task_display_state.task_state_clause`
2. `task_display_state.validate_state_filter`
3. `query_limits.CollectionLimitExceededError`
4. `task_service.TaskService.load_owner_names`
5. `task_service.TaskService`

## Touches

- [project_service](../modules/project_service.md)
- [query_limits](../modules/query_limits.md)
- [task_display_state](../modules/task_display_state.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `project_service.ProjectService._get_tasks_in_state`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
