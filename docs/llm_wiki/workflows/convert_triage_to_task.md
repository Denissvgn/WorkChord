# convert_triage_to_task

**Entry point:** `mcp_agent_tools.convert_triage_to_task`
**Modules involved:** [mcp_agent_tools](../modules/mcp_agent_tools.md), [schemas_triage](../modules/schemas_triage.md), [task_service](../modules/task_service.md), [triage_service](../modules/triage_service.md)

> MCP handler: idempotently convert one locked triage item to one task.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `schemas_triage.TriageConvertToTaskRequest`
2. `triage_service.TriageService`
3. `schemas_triage.TriageConvertToTaskResponse`
4. `task_service.TaskService`

## Touches

- [mcp_agent_tools](../modules/mcp_agent_tools.md)
- [schemas_triage](../modules/schemas_triage.md)
- [task_service](../modules/task_service.md)
- [triage_service](../modules/triage_service.md)

## Behavior

This workflow starts at `mcp_agent_tools.convert_triage_to_task`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
