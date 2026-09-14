# AgentWorkService_review

**Entry point:** `agent_work_service.AgentWorkService.review`
**Modules involved:** [agent_routing_observability](../modules/agent_routing_observability.md), [agent_routing_policy](../modules/agent_routing_policy.md), [agent_routing_service](../modules/agent_routing_service.md), [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [models_agent](../modules/models_agent.md), [schemas_agent](../modules/schemas_agent.md), [task_service](../modules/task_service.md), [time](../modules/time.md)

> Apply an independent verification verdict and optional rework handback.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.validate_idempotency_key`
2. `agent_service.actor_has_scope`
3. `agent_service.AgentPermissionError`
4. `agent_service.AgentConflictError`
5. `agent_service.AgentPermissionError`
6. `agent_service.AgentConflictError`
7. `agent_service.AgentConflictError`
8. `agent_routing_service.AgentRoutingConflictError`
9. `agent_service.actor_has_scope`
10. `agent_service.AgentPermissionError`
11. `agent_service.AgentConflictError`
12. `agent_service.AgentConflictError`
13. `agent_service.AgentConflictError`
14. `agent_service.AgentConflictError`
15. `time.as_utc`
16. `time.as_utc`
17. `time.utc_now`
18. `agent_service.AgentConflictError`
19. `agent_service.AgentConflictError`
20. `task_service.TaskVersionConflictError`
21. `agent_service.AgentConflictError`
22. `models_agent.AgentTaskAssignment`
23. `schemas_agent.AgentReviewVerdictResponse`
24. `agent_routing_policy.canonical_routing_json_bytes`
25. `agent_routing_policy.canonical_routing_json_bytes`
26. `agent_routing_observability.record_routing_operational_event`
27. `agent_routing_observability.record_routing_operational_event`

## Touches

- [agent_routing_observability](../modules/agent_routing_observability.md)
- [agent_routing_policy](../modules/agent_routing_policy.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [models_agent](../modules/models_agent.md)
- [schemas_agent](../modules/schemas_agent.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService.review`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
