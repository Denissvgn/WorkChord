# dry_run_iteration_import

**Entry point:** `agent_planning.dry_run_iteration_import`
**Modules involved:** [agent_service](../modules/agent_service.md), [export](../modules/export.md), [mcp_agent_tools](../modules/mcp_agent_tools.md), [routers_agent_planning](../modules/routers_agent_planning.md)

> Return the exact changes a JSON plan import would make; nothing is written.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.require_scope`
2. `export._read_json_upload`
3. `export._validate_import_data`
4. `mcp_agent_tools.preview_iteration_import`

## Touches

- [agent_service](../modules/agent_service.md)
- [export](../modules/export.md)
- [mcp_agent_tools](../modules/mcp_agent_tools.md)
- [routers_agent_planning](../modules/routers_agent_planning.md)

## Behavior

This workflow starts at `agent_planning.dry_run_iteration_import`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
