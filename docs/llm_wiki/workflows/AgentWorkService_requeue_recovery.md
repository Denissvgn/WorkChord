# AgentWorkService_requeue_recovery

**Entry point:** `agent_work_service.AgentWorkService.requeue_recovery`
**Modules involved:** [agent_routing_policy](../modules/agent_routing_policy.md), [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [commands](../modules/commands.md), [models_agent](../modules/models_agent.md), [schemas_agent](../modules/schemas_agent.md), [task_service](../modules/task_service.md), [time](../modules/time.md)

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
11. `agent_service.AgentConflictError`
12. `time.as_utc`
13. `time.as_utc`
14. `agent_service.AgentConflictError`
15. `agent_service.AgentConflictError`
16. `agent_service.AgentConflictError`
17. `agent_service.AgentConflictError`
18. `models_agent.AgentTaskAssignment`
19. `schemas_agent.AgentRecoveryRequeueResponse`
20. `agent_routing_policy.canonical_routing_json_bytes`
21. `commands.commit_or_flush`

## Touches

- [agent_routing_policy](../modules/agent_routing_policy.md)
- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [commands](../modules/commands.md)
- [models_agent](../modules/models_agent.md)
- [schemas_agent](../modules/schemas_agent.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService.requeue_recovery`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
