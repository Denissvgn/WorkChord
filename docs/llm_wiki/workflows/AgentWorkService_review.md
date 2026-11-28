# AgentWorkService_review

**Entry point:** `agent_work_service.AgentWorkService.review`
**Modules involved:** [agent_routing_observability](../modules/agent_routing_observability.md), [agent_routing_policy](../modules/agent_routing_policy.md), [agent_routing_service](../modules/agent_routing_service.md), [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [commands](../modules/commands.md), [execution_planning_window](../modules/execution_planning_window.md), [models_agent](../modules/models_agent.md), [review_provenance](../modules/review_provenance.md), [schemas_agent](../modules/schemas_agent.md), [task_brief_service](../modules/task_brief_service.md), [task_service](../modules/task_service.md), [time](../modules/time.md)

> Apply an independent verification verdict and optional rework handback.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.validate_idempotency_key`
2. `agent_service.AgentPermissionError`
3. `review_provenance.observe_review_candidate`
4. `agent_service.AgentConflictError`
5. `agent_service.AgentPermissionError`
6. `agent_service.AgentConflictError`
7. `agent_service.AgentConflictError`
8. `agent_routing_service.AgentRoutingConflictError`
9. `agent_service.AgentPermissionError`
10. `agent_service.AgentConflictError`
11. `agent_service.AgentConflictError`
12. `agent_service.AgentConflictError`
13. `agent_service.AgentConflictError`
14. `time.as_utc`
15. `time.as_utc`
16. `time.utc_now`
17. `agent_service.AgentConflictError`
18. `execution_planning_window.assignment_matches`
19. `agent_service.AgentConflictError`
20. `execution_planning_window.require_window_authority`
21. `task_service.TaskVersionConflictError`
22. `review_provenance.different_publisher_required`
23. `review_provenance.verify_verdict`
24. `review_provenance.require_independent_profile`
25. `task_brief_service.TaskBriefService.require_review`
26. `task_brief_service.TaskBriefService`
27. `agent_service.AgentConflictError`
28. `models_agent.AgentTaskAssignment`
29. `schemas_agent.AgentReviewVerdictResponse`
30. `agent_routing_policy.canonical_routing_json_bytes`
31. `agent_routing_policy.canonical_routing_json_bytes`
32. `agent_routing_observability.record_routing_operational_event`
33. `agent_routing_observability.record_routing_operational_event`
34. `commands.commit_or_flush`

## Touches

- [agent_routing_observability](../modules/agent_routing_observability.md)
- [agent_routing_policy](../modules/agent_routing_policy.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [commands](../modules/commands.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [models_agent](../modules/models_agent.md)
- [review_provenance](../modules/review_provenance.md)
- [schemas_agent](../modules/schemas_agent.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Behavior

The assigned verifier reports its observed model with the verdict. Where publisher independence is required, a pass also identifies the exact candidate digest. Before acceptance, the service revalidates the reviewer binding, contributor history, artifact revisions and applicable GitHub head or commit range. The verdict records the inspected task version alongside the brief and artifact revisions, separately from the task version produced by the transition.
