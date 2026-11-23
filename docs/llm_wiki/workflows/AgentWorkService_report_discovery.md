# AgentWorkService_report_discovery

**Entry point:** `agent_work_service.AgentWorkService.report_discovery`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [commands](../modules/commands.md), [execution_planning_window](../modules/execution_planning_window.md), [schemas_triage](../modules/schemas_triage.md), [task_service](../modules/task_service.md), [triage_service](../modules/triage_service.md)

> Create one claim-bound discovery Triage item without expanding scope.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.validate_idempotency_key`
2. `agent_service.AgentPermissionError`
3. `agent_service.AgentPermissionError`
4. `agent_service.AgentPermissionError`
5. `agent_service.AgentPermissionError`
6. `agent_service.AgentConflictError`
7. `agent_service.AgentConflictError`
8. `agent_service.AgentConflictError`
9. `execution_planning_window.assignment_matches`
10. `agent_service.AgentConflictError`
11. `execution_planning_window.require_window_authority`
12. `task_service.TaskVersionConflictError`
13. `triage_service.TriageService.create`
14. `triage_service.TriageService`
15. `schemas_triage.TriageItemCreate`
16. `commands.commit_or_flush`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [commands](../modules/commands.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [schemas_triage](../modules/schemas_triage.md)
- [task_service](../modules/task_service.md)
- [triage_service](../modules/triage_service.md)

## Behavior

An assigned worker can report a discovery while it holds the live task claim. The service verifies the accepted assignment, running execution and task version, then permits one agent-discovery triage item with the task’s project and iteration hints. The item records its source task, assignment, run and actor so the controller can assess it separately.
