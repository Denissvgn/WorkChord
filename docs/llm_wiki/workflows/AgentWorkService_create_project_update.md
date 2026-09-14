# AgentWorkService_create_project_update

**Entry point:** `agent_work_service.AgentWorkService.create_project_update`
**Modules involved:** [agent_service](../modules/agent_service.md), [agent_work_service](../modules/agent_work_service.md), [project_service](../modules/project_service.md), [schemas_project](../modules/schemas_project.md)

> Append one evidence-backed project update with agent attribution.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `agent_service.validate_idempotency_key`
2. `agent_service.AgentConflictError`
3. `project_service.ProjectService`
4. `schemas_project.ProjectUpdateEntryCreate`

## Touches

- [agent_service](../modules/agent_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [project_service](../modules/project_service.md)
- [schemas_project](../modules/schemas_project.md)

## Behavior

This workflow starts at `agent_work_service.AgentWorkService.create_project_update`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
