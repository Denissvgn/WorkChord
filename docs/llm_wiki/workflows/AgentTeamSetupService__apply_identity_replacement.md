# AgentTeamSetupService__apply_identity_replacement

**Entry point:** `agent_team_setup_service.AgentTeamSetupService._apply_identity_replacement`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_team_credentials](../modules/agent_team_credentials.md), [agent_team_setup](../modules/agent_team_setup.md), [agent_team_setup_service](../modules/agent_team_setup_service.md), [commands](../modules/commands.md), [models_agent](../modules/models_agent.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_team_setup.AgentTeamActionReceipt`
2. `agent_team_setup.AgentTeamActionReceipt`
3. `agent_team_credentials.CredentialDeliveryError`
4. `models_agent.AgentActor`
5. `agent_service.hash_api_key`
6. `commands.commit_or_flush`
7. `commands.commit_or_flush`
8. `agent_team_setup.AgentTeamActionReceipt`
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

This workflow starts at `agent_team_setup_service.AgentTeamSetupService._apply_identity_replacement`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
