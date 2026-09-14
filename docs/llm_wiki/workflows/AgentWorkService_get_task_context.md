# AgentWorkService_get_task_context

**Entry point:** `agent_work_service.AgentWorkService.get_task_context`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [schemas_agent](../modules/schemas_agent.md), [time](../modules/time.md)

> Return complete worker context with brief and dependency states.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.actor_has_scope`
2. `agent_service.actor_has_scope`
3. `agent_service.AgentPermissionError`
4. `agent_service.AgentPermissionError`
5. `agent_service.actor_has_scope`
6. `agent_service.actor_has_scope`
7. `agent_service.AgentPermissionError`
8. `time.utc_now`
9. `schemas_agent.AgentDependencyContext`
10. `agent_service.AgentService`
11. `schemas_agent.AgentTaskContextResponse`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [schemas_agent](../modules/schemas_agent.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService.get_task_context`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
