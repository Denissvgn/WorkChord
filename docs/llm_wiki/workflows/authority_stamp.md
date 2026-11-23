# authority_stamp

**Entry point:** `execution_planning_window.authority_stamp`
**Modules involved:** [agent_team_setup_service](../modules/agent_team_setup_service.md), [authority](../modules/authority.md), [config](../modules/config.md), [execution_planning_window](../modules/execution_planning_window.md)

> Fingerprint the actual scope, roster and bindings of both assignment principals.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `authority.internal_authority`
3. `agent_team_setup_service._digest`
4. `agent_team_setup_service._digest`

## Touches

- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [execution_planning_window](../modules/execution_planning_window.md)

## Behavior

This workflow starts at `execution_planning_window.authority_stamp`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
