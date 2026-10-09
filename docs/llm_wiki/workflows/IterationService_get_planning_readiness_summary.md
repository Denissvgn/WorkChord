# IterationService_get_planning_readiness_summary

**Entry point:** `iteration_service.IterationService.get_planning_readiness_summary`
**Modules involved:** [capacity_service](../modules/capacity_service.md), [iteration_service](../modules/iteration_service.md), [schemas_iteration](../modules/schemas_iteration.md), [services_work_metrics](../modules/services_work_metrics.md), [team_service](../modules/team_service.md)

> Return bounded aggregate planning inputs without loading task graphs.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `services_work_metrics.working_today`
2. `services_work_metrics.included_work_ids`
3. `team_service.TeamService`
4. `team_service.TeamService`
5. `capacity_service.CapacityService`
6. `schemas_iteration.IterationPlanningReadinessSummary`

## Touches

- [capacity_service](../modules/capacity_service.md)
- [iteration_service](../modules/iteration_service.md)
- [schemas_iteration](../modules/schemas_iteration.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [team_service](../modules/team_service.md)

## Behavior

This workflow starts at `iteration_service.IterationService.get_planning_readiness_summary`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
