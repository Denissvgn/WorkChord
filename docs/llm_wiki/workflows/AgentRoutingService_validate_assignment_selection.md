# AgentRoutingService_validate_assignment_selection

**Entry point:** `agent_routing_service.AgentRoutingService.validate_assignment_selection`
**Modules involved:** [agent_routing](../modules/agent_routing.md), [agent_routing_policy](../modules/agent_routing_policy.md), [agent_routing_service](../modules/agent_routing_service.md), [agent_service](../modules/agent_service.md), [agent_team_setup_service](../modules/agent_team_setup_service.md), [time](../modules/time.md)

> Recompute and freeze one preview selection inside an assignment transaction.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.as_utc`
2. `time.utc_now`
3. `agent_routing.AgentRoutingPreviewCreate`
4. `agent_team_setup_service.AgentTeamSetupService.membership_boundary`
5. `agent_team_setup_service.AgentTeamSetupService`
6. `agent_service.AgentPermissionError`
7. `agent_routing.RoutingDecisionSnapshot`
8. `agent_routing_policy.validate_routing_packet_size`

## Touches

- [agent_routing](../modules/agent_routing.md)
- [agent_routing_policy](../modules/agent_routing_policy.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_routing_service.AgentRoutingService.validate_assignment_selection`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
