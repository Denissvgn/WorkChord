# AgentWorkService_report_discovery

**Entry point:** `agent_work_service.AgentWorkService.report_discovery`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [schemas_triage](../modules/schemas_triage.md), [task_service](../modules/task_service.md), [triage_service](../modules/triage_service.md)

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
9. `agent_service.AgentConflictError`
10. `task_service.TaskVersionConflictError`
11. `triage_service.TriageService`
12. `schemas_triage.TriageItemCreate`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [schemas_triage](../modules/schemas_triage.md)
- [task_service](../modules/task_service.md)
- [triage_service](../modules/triage_service.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService.report_discovery`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
