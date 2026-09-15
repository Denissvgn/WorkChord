# AgentTeamSetupService__apply_create_or_update

**Entry point:** `agent_team_setup_service.AgentTeamSetupService._apply_create_or_update`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_team_setup](../modules/agent_team_setup.md), [agent_team_setup_service](../modules/agent_team_setup_service.md), [commands](../modules/commands.md), [models_agent](../modules/models_agent.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `models_agent.AgentActor`
2. `agent_service.hash_api_key`
3. `models_agent.AgentTeamTopologyMember`
4. `commands.commit_or_flush`
5. `commands.commit_or_flush`
6. `agent_team_setup.AgentTeamActionReceipt`
7. `models_agent.AgentTeamTopologyMember`
8. `commands.commit_or_flush`
9. `agent_team_setup.AgentTeamActionReceipt`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_team_setup](../modules/agent_team_setup.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [commands](../modules/commands.md)
- [models_agent](../modules/models_agent.md)

## Behavior

This workflow starts at `agent_team_setup_service.AgentTeamSetupService._apply_create_or_update`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
