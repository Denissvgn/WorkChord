# AgentRoutingService_preview_task_routing

**Entry point:** `agent_routing_service.AgentRoutingService.preview_task_routing`
**Modules involved:** [agent_routing_observability](../modules/agent_routing_observability.md), [agent_routing_service](../modules/agent_routing_service.md), [agent_service](../modules/agent_service.md), [time](../modules/time.md)

> Return a deterministic preview and stage bounded shadow/audit evidence.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.AgentPermissionError`
2. `time.utc_now`
3. `agent_routing_observability.routing_exclusion_projection`
4. `agent_routing_observability.record_routing_operational_event`
5. `agent_routing_observability.record_routing_operational_event`

## Touches

- [agent_routing_observability](../modules/agent_routing_observability.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_routing_service.AgentRoutingService.preview_task_routing`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
