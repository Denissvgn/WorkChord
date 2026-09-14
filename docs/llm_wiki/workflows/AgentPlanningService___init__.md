# AgentPlanningService___init__

**Entry point:** `agent_planning_service.AgentPlanningService.__init__`
**Modules involved:** [agent_planning_service](../modules/agent_planning_service.md), [agent_profile_catalog_service](../modules/agent_profile_catalog_service.md), [iteration_service](../modules/iteration_service.md), [project_service](../modules/project_service.md), [scheduler_service](../modules/scheduler_service.md), [task_service](../modules/task_service.md), [team_service](../modules/team_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `project_service.ProjectService`
2. `iteration_service.IterationService`
3. `team_service.TeamService`
4. `scheduler_service.SchedulerService`
5. `task_service.TaskService`
6. `agent_profile_catalog_service.AgentProfileCatalogService`

## Touches

- [agent_planning_service](../modules/agent_planning_service.md)
- [agent_profile_catalog_service](../modules/agent_profile_catalog_service.md)
- [iteration_service](../modules/iteration_service.md)
- [project_service](../modules/project_service.md)
- [scheduler_service](../modules/scheduler_service.md)
- [task_service](../modules/task_service.md)
- [team_service](../modules/team_service.md)

## Behavior

This workflow starts at `agent_planning_service.AgentPlanningService.__init__`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
