# update_task

**Entry point:** `mcp_agent_tools.update_task`
**Modules involved:** [agent_service](../modules/agent_service.md), [mcp_agent_tools](../modules/mcp_agent_tools.md), [mutation_versions](../modules/mutation_versions.md), [schemas_agent](../modules/schemas_agent.md)

> MCP handler: update a task.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `mutation_versions.require_mutation_revision`
2. `agent_service.AgentService`
3. `schemas_agent.AgentTaskPatch`

## Touches

- [agent_service](../modules/agent_service.md)
- [mcp_agent_tools](../modules/mcp_agent_tools.md)
- [mutation_versions](../modules/mutation_versions.md)
- [schemas_agent](../modules/schemas_agent.md)

## Behavior

This workflow starts at `mcp_agent_tools.update_task`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
