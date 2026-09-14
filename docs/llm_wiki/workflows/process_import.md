# process_import

**Entry point:** `export._process_import`
**Modules involved:** [export](../modules/export.md), [models_task](../modules/models_task.md), [schemas_common](../modules/schemas_common.md), [schemas_team](../modules/schemas_team.md), [task_service](../modules/task_service.md), [team_service](../modules/team_service.md)

> Import team members and tasks while preserving task metadata and dependencies.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `team_service.TeamService`
2. `schemas_team.TeamMemberCreate`
3. `schemas_team.VacationCreate`
4. `task_service.TaskService`
5. `models_task.TaskDependency`
6. `schemas_common.MessageResponse`

## Touches

- [export](../modules/export.md)
- [models_task](../modules/models_task.md)
- [schemas_common](../modules/schemas_common.md)
- [schemas_team](../modules/schemas_team.md)
- [task_service](../modules/task_service.md)
- [team_service](../modules/team_service.md)

## Behavior

This workflow starts at `export._process_import`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
