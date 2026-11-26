# convert_triage_to_backlog

**Entry point:** `mcp_agent_tools.convert_triage_to_backlog`
**Modules involved:** [mcp_agent_tools](../modules/mcp_agent_tools.md), [schemas_triage](../modules/schemas_triage.md), [task_service](../modules/task_service.md), [triage_service](../modules/triage_service.md)

> Use an explicit project backlog destination while preserving legacy conversion.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `triage_service.TriageService.convert_to_task`
2. `triage_service.TriageService`
3. `schemas_triage.TriageConvertToTaskResponse`
4. `task_service.TaskService.task_to_response`
5. `task_service.TaskService`
6. `schemas_triage.TriageSourceLinkOutcome.for_link`

## Touches

- [mcp_agent_tools](../modules/mcp_agent_tools.md)
- [schemas_triage](../modules/schemas_triage.md)
- [task_service](../modules/task_service.md)
- [triage_service](../modules/triage_service.md)

## Behavior

This workflow starts at `mcp_agent_tools.convert_triage_to_backlog`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
