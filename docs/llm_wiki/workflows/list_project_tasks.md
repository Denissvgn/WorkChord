# list_project_tasks

**Entry point:** `mcp_agent_tools.list_project_tasks`
**Modules involved:** [mcp_agent_tools](../modules/mcp_agent_tools.md), [project_service](../modules/project_service.md), [task_display_state](../modules/task_display_state.md), [task_service](../modules/task_service.md)

> MCP handler: list tasks linked to a project, or those shown in one state.

``status`` is a displayed state: planned, active, resolved, closed, postponed, canceled or
superseded. With it the result is a flat list of the tasks at any depth shown in that state.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `task_display_state.validate_state_filter`
2. `project_service.ProjectService.get_tasks`
3. `project_service.ProjectService`
4. `task_service.TaskService`
5. `task_service.TaskService.task_to_response`

## Touches

- [mcp_agent_tools](../modules/mcp_agent_tools.md)
- [project_service](../modules/project_service.md)
- [task_display_state](../modules/task_display_state.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `mcp_agent_tools.list_project_tasks`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
