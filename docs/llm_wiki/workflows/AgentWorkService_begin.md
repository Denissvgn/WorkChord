# AgentWorkService_begin

**Entry point:** `agent_work_service.AgentWorkService.begin`
**Modules involved:** [agent_routing_observability](../modules/agent_routing_observability.md), [agent_routing_service](../modules/agent_routing_service.md), [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [commands](../modules/commands.md), [models_agent](../modules/models_agent.md), [review_provenance](../modules/review_provenance.md), [schemas_agent](../modules/schemas_agent.md), [task_service](../modules/task_service.md), [time](../modules/time.md)

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
8. `review_provenance.ReworkReadCache`
9. `agent_routing_service.AgentRoutingConflictError`
10. `agent_routing_service.AgentRoutingConflictError`
11. `agent_routing_service.AgentRoutingConflictError`
12. `agent_routing_service.AgentRoutingConflictError`
13. `agent_routing_observability.record_routing_operational_event`
14. `agent_routing_service.AgentRoutingConflictError`
15. `agent_routing_observability.record_routing_operational_event`
16. `agent_routing_service.AgentRoutingConflictError`
17. `agent_routing_observability.opaque_value_digest`
18. `agent_service.AgentConflictError`
19. `agent_service.AgentConflictError`
20. `task_service.TaskVersionConflictError`
21. `time.utc_now`
22. `agent_service.AgentConflictError`
23. `time.utc_now`
24. `agent_service.AgentConflictError`
25. `review_provenance.different_publisher_required`
26. `review_provenance.actor_provenance`
27. `agent_routing_service.AgentRoutingConflictError`
28. `review_provenance.rework_binding_identity`
29. `agent_routing_service.AgentRoutingConflictError`
30. `models_agent.AgentRun`
31. `schemas_agent.declared_harness`
32. `schemas_agent.declared_harness`
33. `schemas_agent.AgentWorkBeginResponse`
34. `commands.commit_or_flush`

## Touches

- [agent_routing_observability](../modules/agent_routing_observability.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [commands](../modules/commands.md)
- [models_agent](../modules/models_agent.md)
- [review_provenance](../modules/review_provenance.md)
- [schemas_agent](../modules/schemas_agent.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Behavior

The worker presents the server-selected assignment and current queue revision. Begin rechecks task readiness and routing state, then creates the next claim generation and its run in one transaction. When the project requires different publishers for implementation and review, begin also requires a worker profile and an observed model that resolves to a publisher.
