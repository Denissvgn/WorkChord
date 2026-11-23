# check_supervised_selection

**Entry point:** `review_evidence.check_supervised_selection`
**Modules involved:** [agent_routing](../modules/agent_routing.md), [agent_routing_service](../modules/agent_routing_service.md), [services_review_evidence](../modules/services_review_evidence.md), [time](../modules/time.md)

> Supervised dispatch must also produce a positive live route for an evidence-backed verifier.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_routing_service.AgentRoutingService`
2. `agent_routing_service.AgentRoutingService._require_preview_rollout`
3. `agent_routing.AgentRoutingPreviewCreate`
4. `agent_routing_service.AgentRoutingService._build_preview`
5. `time.utc_now`

## Touches

- [agent_routing](../modules/agent_routing.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [services_review_evidence](../modules/services_review_evidence.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `review_evidence.check_supervised_selection`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
