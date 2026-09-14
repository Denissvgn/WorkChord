# AgentWorkService_begin

**Entry point:** `agent_work_service.AgentWorkService.begin`
**Modules involved:** [agent_routing_observability](../modules/agent_routing_observability.md), [agent_routing_service](../modules/agent_routing_service.md), [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [models_agent](../modules/models_agent.md), [schemas_agent](../modules/schemas_agent.md), [task_service](../modules/task_service.md), [time](../modules/time.md)

> Atomically accept, fence, claim, run, and activate selected work.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.validate_idempotency_key`
2. `agent_service.AgentPermissionError`
3. `agent_service.AgentPermissionError`
4. `agent_service.AgentPermissionError`
5. `agent_service.AgentPermissionError`
6. `agent_service.AgentConflictError`
7. `agent_service.AgentConflictError`
8. `agent_routing_service.AgentRoutingConflictError`
9. `agent_routing_service.AgentRoutingConflictError`
10. `agent_routing_service.AgentRoutingConflictError`
11. `agent_routing_observability.record_routing_operational_event`
12. `agent_routing_service.AgentRoutingConflictError`
13. `agent_routing_observability.record_routing_operational_event`
14. `agent_routing_service.AgentRoutingConflictError`
15. `agent_routing_observability.opaque_value_digest`
16. `agent_service.AgentConflictError`
17. `agent_service.AgentConflictError`
18. `task_service.TaskVersionConflictError`
19. `time.utc_now`
20. `agent_service.AgentConflictError`
21. `time.utc_now`
22. `agent_service.AgentConflictError`
23. `models_agent.AgentRun`
24. `schemas_agent.AgentWorkBeginResponse`

## Touches

- [agent_routing_observability](../modules/agent_routing_observability.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [models_agent](../modules/models_agent.md)
- [schemas_agent](../modules/schemas_agent.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService.begin`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
