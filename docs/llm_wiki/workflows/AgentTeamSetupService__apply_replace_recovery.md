# AgentTeamSetupService__apply_replace_recovery

**Entry point:** `agent_team_setup_service.AgentTeamSetupService._apply_replace_recovery`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_team_credentials](../modules/agent_team_credentials.md), [agent_team_setup](../modules/agent_team_setup.md), [agent_team_setup_service](../modules/agent_team_setup_service.md), [commands](../modules/commands.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_team_setup.AgentTeamActionReceipt`
2. `agent_team_setup.load_stored_agent_team_member`
3. `agent_team_setup.AgentTeamActionReceipt`
4. `agent_team_setup.AgentTeamActionReceipt`
5. `agent_team_credentials.CredentialDeliveryError`
6. `agent_service.hash_api_key`
7. `commands.commit_or_flush`
8. `commands.commit_or_flush`
9. `agent_team_credentials.CredentialDeliveryError`
10. `commands.commit_or_flush`
11. `agent_team_setup.AgentTeamActionReceipt`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_team_credentials](../modules/agent_team_credentials.md)
- [agent_team_setup](../modules/agent_team_setup.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [commands](../modules/commands.md)

## Behavior

This workflow starts at `agent_team_setup_service.AgentTeamSetupService._apply_replace_recovery`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.

Recovery normally accepts a change of `credential_ref` only. When the stored contract breaks today's role rules, it also accepts the role-governed fields (`scope_preset`, `assignment_modes`, `skill_package`) of the current master, so one approved recovery delivers a new credential and brings the contract up to date. Any other drift is refused with `credential_recovery_change_not_isolated`.
