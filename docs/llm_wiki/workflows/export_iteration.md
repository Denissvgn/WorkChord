# export_iteration

**Entry point:** `export.export_iteration`
**Modules involved:** [export](../modules/export.md), [iteration_service](../modules/iteration_service.md), [task_service](../modules/task_service.md), [team_service](../modules/team_service.md)

> Export iteration data as JSON.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `iteration_service.IterationService`
2. `task_service.TaskService`
3. `team_service.TeamService`

## Touches

- [export](../modules/export.md)
- [iteration_service](../modules/iteration_service.md)
- [task_service](../modules/task_service.md)
- [team_service](../modules/team_service.md)

## Behavior

This workflow starts at `export.export_iteration`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
