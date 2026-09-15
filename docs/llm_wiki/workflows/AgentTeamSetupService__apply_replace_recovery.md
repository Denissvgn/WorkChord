# AgentTeamSetupService__apply_replace_recovery

**Entry point:** `agent_team_setup_service.AgentTeamSetupService._apply_replace_recovery`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_team_setup](../modules/agent_team_setup.md), [agent_team_setup_service](../modules/agent_team_setup_service.md), [commands](../modules/commands.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_team_setup.AgentTeamActionReceipt`
2. `agent_team_setup.AgentTeamActionReceipt`
3. `agent_team_setup.AgentTeamActionReceipt`
4. `agent_service.hash_api_key`
5. `commands.commit_or_flush`
6. `commands.commit_or_flush`
7. `commands.commit_or_flush`
8. `agent_team_setup.AgentTeamActionReceipt`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_team_setup](../modules/agent_team_setup.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [commands](../modules/commands.md)

## Behavior

This workflow starts at `agent_team_setup_service.AgentTeamSetupService._apply_replace_recovery`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
