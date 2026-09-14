# AgentTeamSetupService_apply

**Entry point:** `agent_team_setup_service.AgentTeamSetupService.apply`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_team_setup](../modules/agent_team_setup.md), [agent_team_setup_service](../modules/agent_team_setup_service.md), [models_agent](../modules/models_agent.md)

> Apply only exact approved action IDs and persist resumable receipts.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.validate_idempotency_key`
2. `agent_team_setup.parse_agent_team_master`
3. `agent_team_setup.AgentTeamPlanRequest`
4. `models_agent.AgentTeamApplyRun`
5. `agent_team_setup.AgentTeamActionReceipt`
6. `agent_team_setup.AgentTeamApplyResponse`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_team_setup](../modules/agent_team_setup.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [models_agent](../modules/models_agent.md)

## Behavior

This workflow starts at `agent_team_setup_service.AgentTeamSetupService.apply`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
