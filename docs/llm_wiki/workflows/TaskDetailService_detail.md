# TaskDetailService_detail

**Entry point:** `task_detail_service.TaskDetailService.detail`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [schemas_task](../modules/schemas_task.md), [task_detail](../modules/task_detail.md), [task_detail_service](../modules/task_detail_service.md), [task_service](../modules/task_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `task_service.TaskService.load_owner_names`
3. `task_service.TaskService`
4. `task_service.TaskService.task_to_response`
5. `task_service.TaskService`
6. `schemas_task.TaskAgentReadiness`
7. `commands.PlanningConflict`
8. `task_detail.TaskDetailResponse`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [schemas_task](../modules/schemas_task.md)
- [task_detail](../modules/task_detail.md)
- [task_detail_service](../modules/task_detail_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `task_detail_service.TaskDetailService.detail`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
