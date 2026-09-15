# AgentWorkService_create_assignment

**Entry point:** `agent_work_service.AgentWorkService.create_assignment`
**Modules involved:** [agent_routing_service](../modules/agent_routing_service.md), [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [commands](../modules/commands.md), [models_agent](../modules/models_agent.md), [task_service](../modules/task_service.md), [time](../modules/time.md)

> Dispatch one task to one provisioned actor.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.validate_idempotency_key`
2. `agent_routing_service.AgentRoutingService`
3. `agent_service.AgentConflictError`
4. `task_service.TaskVersionConflictError`
5. `agent_service.AgentConflictError`
6. `agent_service.AgentConflictError`
7. `agent_service.AgentConflictError`
8. `agent_service.AgentConflictError`
9. `time.utc_now`
10. `models_agent.AgentTaskAssignment`
11. `commands.commit_or_flush`

## Touches

- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [commands](../modules/commands.md)
- [models_agent](../modules/models_agent.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService.create_assignment`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
