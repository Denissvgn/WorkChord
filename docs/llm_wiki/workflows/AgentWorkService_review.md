# AgentWorkService_review

**Entry point:** `agent_work_service.AgentWorkService.review`
**Modules involved:** [agent_routing_observability](../modules/agent_routing_observability.md), [agent_routing_policy](../modules/agent_routing_policy.md), [agent_routing_service](../modules/agent_routing_service.md), [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [commands](../modules/commands.md), [models_agent](../modules/models_agent.md), [review_provenance](../modules/review_provenance.md), [schemas_agent](../modules/schemas_agent.md), [task_brief_service](../modules/task_brief_service.md), [task_service](../modules/task_service.md), [time](../modules/time.md)

> Apply an independent verification verdict and optional rework handback.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.validate_idempotency_key`
2. `agent_service.actor_has_scope`
3. `agent_service.AgentPermissionError`
4. `review_provenance.observe_review_candidate`
5. `agent_service.AgentConflictError`
6. `agent_service.AgentPermissionError`
7. `agent_service.AgentConflictError`
8. `agent_service.AgentConflictError`
9. `agent_routing_service.AgentRoutingConflictError`
10. `agent_service.actor_has_scope`
11. `agent_service.AgentPermissionError`
12. `agent_service.AgentConflictError`
13. `agent_service.AgentConflictError`
14. `agent_service.AgentConflictError`
15. `agent_service.AgentConflictError`
16. `time.as_utc`
17. `time.as_utc`
18. `time.utc_now`
19. `agent_service.AgentConflictError`
20. `agent_service.AgentConflictError`
21. `task_service.TaskVersionConflictError`
22. `review_provenance.different_publisher_required`
23. `review_provenance.verify_verdict`
24. `task_brief_service.TaskBriefService.require_review`
25. `task_brief_service.TaskBriefService`
26. `task_brief_service.TaskBriefService.record_review`
27. `task_brief_service.TaskBriefService`
28. `agent_service.AgentConflictError`
29. `models_agent.AgentTaskAssignment`
30. `schemas_agent.AgentReviewVerdictResponse`
31. `agent_routing_policy.canonical_routing_json_bytes`
32. `agent_routing_policy.canonical_routing_json_bytes`
33. `agent_routing_observability.record_routing_operational_event`
34. `agent_routing_observability.record_routing_operational_event`
35. `commands.commit_or_flush`

## Touches

- [agent_routing_observability](../modules/agent_routing_observability.md)
- [agent_routing_policy](../modules/agent_routing_policy.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [commands](../modules/commands.md)
- [models_agent](../modules/models_agent.md)
- [review_provenance](../modules/review_provenance.md)
- [schemas_agent](../modules/schemas_agent.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Behavior

The assigned verifier reports its observed model with the verdict. Where publisher independence is required, a pass also identifies the exact candidate digest. Before acceptance, the service revalidates the reviewer binding, contributor history, artifact revisions and applicable GitHub head or commit range.
