# create_task_github_link

**Entry point:** `mcp_agent_tools.create_task_github_link`
**Modules involved:** [agent_service](../modules/agent_service.md), [external_link_service](../modules/external_link_service.md), [mcp_agent_tools](../modules/mcp_agent_tools.md), [task_context_revision_service](../modules/task_context_revision_service.md)

> MCP handler: idempotently link a GitHub URL to a task.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `task_context_revision_service.lock_task_context`
2. `external_link_service.ExternalLinkService`
3. `external_link_service.ExternalLinkService.create_task_github_link`
4. `agent_service.AgentConflictError`
5. `external_link_service.ExternalLinkService.link_to_response`

## Touches

- [agent_service](../modules/agent_service.md)
- [external_link_service](../modules/external_link_service.md)
- [mcp_agent_tools](../modules/mcp_agent_tools.md)
- [task_context_revision_service](../modules/task_context_revision_service.md)

## Behavior

This workflow starts at `mcp_agent_tools.create_task_github_link`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
