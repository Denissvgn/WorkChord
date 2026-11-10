# AgentTeamSetupService_acknowledge_runtime

**Entry point:** `agent_team_setup_service.AgentTeamSetupService.acknowledge_runtime`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_team_setup](../modules/agent_team_setup.md), [agent_team_setup_service](../modules/agent_team_setup_service.md), [authority](../modules/authority.md), [commands](../modules/commands.md), [identity_service](../modules/identity_service.md), [models_identity](../modules/models_identity.md), [time](../modules/time.md)

> Accept only the exact restricted onboarding handoff acknowledgement.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.AgentService`
2. `agent_service.AgentService.authenticate_onboarding`
3. `agent_service.AgentService.authenticate`
4. `agent_service.AgentPermissionError`
5. `authority.internal_authority`
6. `agent_service.AgentPermissionError`
7. `models_identity.Principal`
8. `identity_service.bind_verified_system`
9. `agent_service.AgentPermissionError`
10. `agent_team_setup.AgentTeamRuntimeAcknowledgementResponse`
11. `time.utc_now`
12. `time.utc_now`
13. `commands.commit_or_flush`
14. `agent_team_setup.AgentTeamRuntimeAcknowledgementResponse`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_team_setup](../modules/agent_team_setup.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [identity_service](../modules/identity_service.md)
- [models_identity](../modules/models_identity.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_team_setup_service.AgentTeamSetupService.acknowledge_runtime`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
