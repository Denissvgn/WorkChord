# require_agent_read_access

**Entry point:** `agent.require_agent_read_access`
**Modules involved:** [agent_service](../modules/agent_service.md), [config](../modules/config.md), [routers_agent](../modules/routers_agent.md), [security](../modules/security.md)

> Allow pipeline reads from a configured admin key or scoped agent key.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `security.admin_api_key_is_valid`
2. `config.get_settings`
3. `agent_service.require_scope`

## Touches

- [agent_service](../modules/agent_service.md)
- [config](../modules/config.md)
- [routers_agent](../modules/routers_agent.md)
- [security](../modules/security.md)

## Behavior

This workflow starts at `agent.require_agent_read_access`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
