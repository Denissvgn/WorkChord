# AgentWorkService__terminal_work

**Entry point:** `agent_work_service.AgentWorkService._terminal_work`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [schemas_agent](../modules/schemas_agent.md), [task_service](../modules/task_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.validate_idempotency_key`
2. `agent_service.AgentPermissionError`
3. `agent_service.AgentPermissionError`
4. `agent_service.AgentPermissionError`
5. `agent_service.AgentPermissionError`
6. `agent_service.AgentConflictError`
7. `agent_service.AgentConflictError`
8. `agent_service.AgentPermissionError`
9. `agent_service.AgentConflictError`
10. `agent_service.AgentConflictError`
11. `task_service.TaskVersionConflictError`
12. `time.utc_now`
13. `agent_service.AgentConflictError`
14. `schemas_agent.AgentWorkTerminalResponse`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [schemas_agent](../modules/schemas_agent.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService._terminal_work`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
