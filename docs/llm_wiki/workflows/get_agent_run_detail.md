# get_agent_run_detail

**Entry point:** `mcp_agent_tools.get_agent_run_detail`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [mcp_agent_tools](../modules/mcp_agent_tools.md), [schemas_agent](../modules/schemas_agent.md)

> MCP handler: return one run and its chronological events.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.AgentService`
2. `agent_work_service.AgentWorkService.run_response`
3. `schemas_agent.AgentRunEventResponse`
4. `schemas_agent.AgentRunDetailResponse`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [mcp_agent_tools](../modules/mcp_agent_tools.md)
- [schemas_agent](../modules/schemas_agent.md)

## Behavior

This workflow starts at `mcp_agent_tools.get_agent_run_detail`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
