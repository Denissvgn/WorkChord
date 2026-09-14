# AgentWorkService_update_assignment

**Entry point:** `agent_work_service.AgentWorkService.update_assignment`
**Modules involved:** [agent_routing_service](../modules/agent_routing_service.md), [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [time](../modules/time.md)

> Reassign, reorder, or cancel queued work.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.validate_idempotency_key`
2. `agent_routing_service.AgentRoutingService`
3. `agent_service.AgentConflictError`
4. `agent_service.AgentConflictError`
5. `agent_service.AgentConflictError`
6. `agent_service.AgentConflictError`
7. `agent_service.AgentConflictError`
8. `agent_service.AgentConflictError`
9. `agent_service.AgentConflictError`
10. `agent_service.AgentConflictError`
11. `agent_routing_service.AgentRoutingConflictError`
12. `time.utc_now`
13. `agent_routing_service.AgentRoutingConflictError`

## Touches

- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService.update_assignment`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
