# AgentRoutingService__require_preview_rollout

**Entry point:** `agent_routing_service.AgentRoutingService._require_preview_rollout`
**Modules involved:** [agent_routing_rollout](../modules/agent_routing_rollout.md), [agent_routing_service](../modules/agent_routing_service.md), [agent_team_setup_service](../modules/agent_team_setup_service.md), [refusal_next_steps](../modules/refusal_next_steps.md)

> Translate fail-closed rollout state into the routing error envelope.

With ``verifier_actor_id`` a verification preview needs only that verifier to be present. The refusal
names non-ready actors only of a team the caller belongs to, or of the verifier's team for a caller
with authority over the task's project.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_routing_rollout.AgentRoutingRolloutService`
2. `agent_team_setup_service.AgentTeamSetupService.readiness_gate`
3. `agent_team_setup_service.AgentTeamSetupService`
4. `agent_routing_rollout.AgentRoutingRolloutService`
5. `agent_routing_rollout.AgentRoutingRolloutService`
6. `refusal_next_steps.next_step_for`

## Touches

- [agent_routing_rollout](../modules/agent_routing_rollout.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [refusal_next_steps](../modules/refusal_next_steps.md)

## Behavior

This workflow starts at `agent_routing_service.AgentRoutingService._require_preview_rollout`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
