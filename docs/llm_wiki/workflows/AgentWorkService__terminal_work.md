# AgentWorkService__terminal_work

**Entry point:** `agent_work_service.AgentWorkService._terminal_work`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [commands](../modules/commands.md), [review_provenance](../modules/review_provenance.md), [schemas_agent](../modules/schemas_agent.md), [schemas_task_brief](../modules/schemas_task_brief.md), [task_brief_service](../modules/task_brief_service.md), [task_service](../modules/task_service.md), [time](../modules/time.md)

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
12. `review_provenance.different_publisher_required`
13. `review_provenance.record_terminal_observation`
14. `time.utc_now`
15. `task_brief_service.TaskBriefService`
16. `schemas_task_brief.ProgressWrite`
17. `agent_service.AgentConflictError`
18. `schemas_agent.AgentWorkTerminalResponse`
19. `commands.commit_or_flush`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [commands](../modules/commands.md)
- [review_provenance](../modules/review_provenance.md)
- [schemas_agent](../modules/schemas_agent.md)
- [schemas_task_brief](../modules/schemas_task_brief.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService._terminal_work`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
