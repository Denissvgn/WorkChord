# AgentService_authenticate_bootstrap_key

**Entry point:** `agent_service.AgentService.authenticate_bootstrap_key`
**Modules involved:** [agent_service](../modules/agent_service.md), [config](../modules/config.md), [models_agent](../modules/models_agent.md), [time](../modules/time.md)

> Return a transient provisioning actor for the bootstrap API key.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `models_agent.AgentActor`
3. `time.utc_now`

## Touches

- [agent_service](../modules/agent_service.md)
- [config](../modules/config.md)
- [models_agent](../modules/models_agent.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_service.AgentService.authenticate_bootstrap_key`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
