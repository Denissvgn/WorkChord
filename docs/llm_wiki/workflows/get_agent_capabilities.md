# get_agent_capabilities

**Entry point:** `agent.get_agent_capabilities`
**Modules involved:** [agent_contract](../modules/agent_contract.md), [agent_routing_rollout](../modules/agent_routing_rollout.md), [agent_service](../modules/agent_service.md), [agent_team_setup_service](../modules/agent_team_setup_service.md), [config](../modules/config.md), [routers_agent](../modules/routers_agent.md), [schemas_agent](../modules/schemas_agent.md)

> Return the authenticated actor and supported agent contract features.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_routing_rollout.AgentRoutingRolloutService`
2. `agent_team_setup_service.AgentTeamSetupService`
3. `agent_routing_rollout.AgentRoutingRolloutService`
4. `agent_routing_rollout.AgentRoutingRolloutService`
5. `agent_contract.agent_contract_features`
6. `config.get_settings`
7. `agent_service.actor_has_scope`
8. `schemas_agent.AgentCapabilitiesResponse`
9. `agent_service.actor_scopes`

## Touches

- [agent_contract](../modules/agent_contract.md)
- [agent_routing_rollout](../modules/agent_routing_rollout.md)
- [agent_service](../modules/agent_service.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [config](../modules/config.md)
- [routers_agent](../modules/routers_agent.md)
- [schemas_agent](../modules/schemas_agent.md)

## Behavior

This workflow starts at `agent.get_agent_capabilities`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
