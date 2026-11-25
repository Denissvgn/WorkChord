# AgentWorkService_begin

**Entry point:** `agent_work_service.AgentWorkService.begin`
**Modules involved:** [agent_routing_observability](../modules/agent_routing_observability.md), [agent_routing_service](../modules/agent_routing_service.md), [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [commands](../modules/commands.md), [execution_planning_window](../modules/execution_planning_window.md), [maintenance_window_service](../modules/maintenance_window_service.md), [models_agent](../modules/models_agent.md), [retained_planning_output](../modules/retained_planning_output.md), [review_provenance](../modules/review_provenance.md), [schemas_agent](../modules/schemas_agent.md), [task_service](../modules/task_service.md), [time](../modules/time.md)

> Atomically accept, fence, claim, run, and activate selected work.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.validate_idempotency_key`
2. `agent_service.AgentPermissionError`
3. `agent_service.AgentPermissionError`
4. `agent_service.AgentPermissionError`
5. `agent_service.AgentPermissionError`
6. `maintenance_window_service.require_start_admission`
7. `agent_service.AgentConflictError`
8. `agent_service.AgentConflictError`
9. `review_provenance.ReworkReadCache`
10. `retained_planning_output.recovery_attestation_hint`
11. `agent_routing_service.AgentRoutingConflictError`
12. `agent_routing_service.AgentRoutingConflictError`
13. `agent_routing_service.AgentRoutingConflictError`
14. `agent_routing_service.AgentRoutingConflictError`
15. `agent_routing_service.AgentRoutingConflictError`
16. `agent_routing_observability.record_routing_operational_event`
17. `agent_routing_service.AgentRoutingConflictError`
18. `agent_routing_observability.record_routing_operational_event`
19. `agent_routing_service.AgentRoutingConflictError`
20. `agent_routing_observability.opaque_value_digest`
21. `agent_service.AgentConflictError`
22. `agent_service.AgentConflictError`
23. `execution_planning_window.assignment_matches`
24. `task_service.TaskVersionConflictError`
25. `execution_planning_window.require_window_authority`
26. `time.utc_now`
27. `agent_service.AgentConflictError`
28. `time.utc_now`
29. `agent_service.AgentConflictError`
30. `review_provenance.different_publisher_required`
31. `review_provenance.actor_provenance`
32. `agent_routing_service.AgentRoutingConflictError`
33. `review_provenance.rework_binding_identity`
34. `agent_routing_service.AgentRoutingConflictError`
35. `models_agent.AgentRun`
36. `schemas_agent.declared_harness`
37. `schemas_agent.declared_harness`
38. `schemas_agent.AgentWorkBeginResponse`
39. `commands.commit_or_flush`

## Touches

- [agent_routing_observability](../modules/agent_routing_observability.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [commands](../modules/commands.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [maintenance_window_service](../modules/maintenance_window_service.md)
- [models_agent](../modules/models_agent.md)
- [retained_planning_output](../modules/retained_planning_output.md)
- [review_provenance](../modules/review_provenance.md)
- [schemas_agent](../modules/schemas_agent.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Behavior

The worker presents the server-selected assignment and current queue revision. Begin rechecks task readiness and routing state, then creates the next claim generation and its run in one transaction. When the project requires different publishers for implementation and review, begin also requires a worker profile and an observed model that resolves to a publisher.
