# create_request_source_link

**Entry point:** `mcp_agent_tools.create_request_source_link`
**Modules involved:** [agent_service](../modules/agent_service.md), [mcp_agent_tools](../modules/mcp_agent_tools.md), [request_source_service](../modules/request_source_service.md), [schemas_request_source](../modules/schemas_request_source.md)

> MCP handler: idempotently create an attributed request-source link.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `schemas_request_source.RequestSourceLinkCreateRequest`
2. `agent_service.AgentConflictError`
3. `request_source_service.RequestSourceService`
4. `agent_service.AgentConflictError`
5. `agent_service.AgentConflictError`

## Touches

- [agent_service](../modules/agent_service.md)
- [mcp_agent_tools](../modules/mcp_agent_tools.md)
- [request_source_service](../modules/request_source_service.md)
- [schemas_request_source](../modules/schemas_request_source.md)

## Behavior

This workflow starts at `mcp_agent_tools.create_request_source_link`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
