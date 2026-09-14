# AgentTeamSetupService_acknowledge_runtime

**Entry point:** `agent_team_setup_service.AgentTeamSetupService.acknowledge_runtime`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_team_setup](../modules/agent_team_setup.md), [agent_team_setup_service](../modules/agent_team_setup_service.md), [time](../modules/time.md)

> Accept only the exact restricted onboarding handoff acknowledgement.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.AgentService`
2. `agent_service.AgentPermissionError`
3. `agent_service.AgentPermissionError`
4. `agent_team_setup.AgentTeamRuntimeAcknowledgementResponse`
5. `time.utc_now`
6. `time.utc_now`
7. `agent_team_setup.AgentTeamRuntimeAcknowledgementResponse`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_team_setup](../modules/agent_team_setup.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_team_setup_service.AgentTeamSetupService.acknowledge_runtime`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
