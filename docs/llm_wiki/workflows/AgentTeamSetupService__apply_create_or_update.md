# AgentTeamSetupService__apply_create_or_update

**Entry point:** `agent_team_setup_service.AgentTeamSetupService._apply_create_or_update`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_team_credentials](../modules/agent_team_credentials.md), [agent_team_setup](../modules/agent_team_setup.md), [agent_team_setup_service](../modules/agent_team_setup_service.md), [commands](../modules/commands.md), [models_agent](../modules/models_agent.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_team_credentials.CredentialDeliveryError`
2. `models_agent.AgentActor`
3. `agent_service.hash_api_key`
4. `models_agent.AgentTeamTopologyMember`
5. `commands.commit_or_flush`
6. `commands.commit_or_flush`
7. `agent_team_setup.AgentTeamActionReceipt`
8. `models_agent.AgentTeamTopologyMember`
9. `commands.commit_or_flush`
10. `agent_team_setup.AgentTeamActionReceipt`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_team_credentials](../modules/agent_team_credentials.md)
- [agent_team_setup](../modules/agent_team_setup.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [commands](../modules/commands.md)
- [models_agent](../modules/models_agent.md)

## Behavior

This workflow starts at `agent_team_setup_service.AgentTeamSetupService._apply_create_or_update`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
