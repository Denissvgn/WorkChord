# AgentWorkService_renew_work

**Entry point:** `agent_work_service.AgentWorkService.renew_work`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [commands](../modules/commands.md), [execution_planning_window](../modules/execution_planning_window.md), [review_provenance](../modules/review_provenance.md), [schemas_agent](../modules/schemas_agent.md), [task_service](../modules/task_service.md), [time](../modules/time.md)

> Atomically renew an accepted assignment's live claim and heartbeat.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.validate_idempotency_key`
2. `agent_service.AgentPermissionError`
3. `agent_service.AgentPermissionError`
4. `agent_service.AgentPermissionError`
5. `agent_service.AgentPermissionError`
6. `agent_service.AgentConflictError`
7. `agent_service.AgentConflictError`
8. `execution_planning_window.assignment_matches`
9. `agent_service.AgentConflictError`
10. `execution_planning_window.require_window_authority`
11. `task_service.TaskVersionConflictError`
12. `agent_service.AgentConflictError`
13. `review_provenance.record_terminal_observation`
14. `time.utc_now`
15. `schemas_agent.AgentWorkBeginResponse`
16. `commands.commit_or_flush`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [commands](../modules/commands.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [review_provenance](../modules/review_provenance.md)
- [schemas_agent](../modules/schemas_agent.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService.renew_work`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
