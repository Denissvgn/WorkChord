# AgentWorkService_requeue_recovery

**Entry point:** `agent_work_service.AgentWorkService.requeue_recovery`
**Modules involved:** [agent_routing_policy](../modules/agent_routing_policy.md), [agent_routing_service](../modules/agent_routing_service.md), [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [commands](../modules/commands.md), [execution_planning_window](../modules/execution_planning_window.md), [models_agent](../modules/models_agent.md), [review_provenance](../modules/review_provenance.md), [schemas_agent](../modules/schemas_agent.md), [task_service](../modules/task_service.md), [time](../modules/time.md)

> Cancel stale ownership and create one ordered recovery assignment.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.validate_idempotency_key`
2. `agent_service.AgentConflictError`
3. `agent_service.AgentConflictError`
4. `task_service.TaskVersionConflictError`
5. `agent_service.AgentConflictError`
6. `time.utc_now`
7. `agent_service.AgentConflictError`
8. `agent_service.AgentConflictError`
9. `agent_service.AgentConflictError`
10. `agent_service.AgentConflictError`
11. `review_provenance.different_publisher_required`
12. `agent_service.AgentConflictError`
13. `agent_service.AgentConflictError`
14. `agent_service.AgentConflictError`
15. `time.as_utc`
16. `time.as_utc`
17. `execution_planning_window.window_authority_matches`
18. `agent_service.AgentConflictError`
19. `agent_service.AgentConflictError`
20. `agent_service.AgentConflictError`
21. `agent_routing_service.AgentRoutingConflictError`
22. `review_provenance.different_publisher_required`
23. `review_provenance.mark_server_interruption`
24. `review_provenance.record_server_end_profile`
25. `commands.current_command`
26. `agent_service.AgentConflictError`
27. `models_agent.AgentTaskAssignment`
28. `schemas_agent.AgentRecoveryRequeueResponse`
29. `agent_routing_policy.canonical_routing_json_bytes`
30. `commands.commit_or_flush`

## Touches

- [agent_routing_policy](../modules/agent_routing_policy.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [commands](../modules/commands.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [models_agent](../modules/models_agent.md)
- [review_provenance](../modules/review_provenance.md)
- [schemas_agent](../modules/schemas_agent.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Behavior

The controller submits the task version, live assignment IDs, running run IDs and claim generation from the recovery list. The service locks the task and owners, compares that tuple and checks team membership before changing a queue. It cancels stale execution, clears the old claim and records one recovery assignment and its audit event. In shadow mode, an explicitly selected worker can begin eligible supervised recovery. Governed history retains its fresh-selection requirement.
