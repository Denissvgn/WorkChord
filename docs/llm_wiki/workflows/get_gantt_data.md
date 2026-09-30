# get_gantt_data

**Entry point:** `gantt.get_gantt_data`
**Modules involved:** [calendar_service](../modules/calendar_service.md), [iteration_service](../modules/iteration_service.md), [routers_gantt](../modules/routers_gantt.md), [schemas_gantt](../modules/schemas_gantt.md), [schemas_iteration](../modules/schemas_iteration.md), [task_service](../modules/task_service.md), [team_service](../modules/team_service.md)

> Get Gantt chart data for an iteration.

Database queries are deliberately sequential because all services share the
request-scoped ``AsyncSession``. SQLAlchemy does not permit concurrent work
on one async session. Vacation dates still use O(1) set lookups.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `iteration_service.IterationService`
2. `task_service.TaskService`
3. `team_service.TeamService`
4. `calendar_service.CalendarService`
5. `schemas_gantt.GanttResponse`
6. `schemas_iteration.IterationResponse`

## Touches

- [calendar_service](../modules/calendar_service.md)
- [iteration_service](../modules/iteration_service.md)
- [routers_gantt](../modules/routers_gantt.md)
- [schemas_gantt](../modules/schemas_gantt.md)
- [schemas_iteration](../modules/schemas_iteration.md)
- [task_service](../modules/task_service.md)
- [team_service](../modules/team_service.md)

## Behavior

This workflow starts at `gantt.get_gantt_data`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
