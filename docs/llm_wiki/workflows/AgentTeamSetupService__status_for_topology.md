# AgentTeamSetupService__status_for_topology

**Entry point:** `agent_team_setup_service.AgentTeamSetupService._status_for_topology`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_team_setup](../modules/agent_team_setup.md), [agent_team_setup_service](../modules/agent_team_setup_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_team_setup.load_stored_agent_team_master`
2. `time.utc_now`
3. `agent_team_setup.AgentTeamMemberLifecycle`
4. `agent_service.actor_scopes`
5. `time.as_utc`
6. `time.as_utc`
7. `agent_team_setup.AgentTeamMemberStatus`
8. `agent_team_setup.AgentTeamSetupStep`
9. `agent_team_setup.AgentTeamSetupStep`
10. `agent_team_setup.AgentTeamSetupStep`
11. `agent_team_setup.AgentTeamSetupStep`
12. `agent_team_setup.AgentTeamSetupStep`
13. `agent_team_setup.AgentTeamSetupStep`
14. `agent_team_setup.AgentTeamSetupStep`
15. `agent_team_setup.AgentTeamStatusResponse`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_team_setup](../modules/agent_team_setup.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_team_setup_service.AgentTeamSetupService._status_for_topology`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.

The stored manifest is read with the stored-contract loader. Each member's contract is judged from its member row, the same contract acknowledgement checks; a member with no row falls back to its manifest entry, and an unreadable row counts as outdated. Outdated members carry `stored_contract_outdated`, are not runtime ready and get no handoff; the topology and the `master` step then carry the same code.
