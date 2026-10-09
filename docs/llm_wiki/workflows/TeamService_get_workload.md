# TeamService_get_workload

**Entry point:** `team_service.TeamService.get_workload`
**Modules involved:** [capacity_service](../modules/capacity_service.md), [schemas_team](../modules/schemas_team.md), [services_work_metrics](../modules/services_work_metrics.md), [team_service](../modules/team_service.md)

> Get workload information for a team member.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `capacity_service.CapacityService`
2. `services_work_metrics.included_work_ids`
3. `schemas_team.MemberWorkload`

## Touches

- [capacity_service](../modules/capacity_service.md)
- [schemas_team](../modules/schemas_team.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [team_service](../modules/team_service.md)

## Behavior

This workflow starts at `team_service.TeamService.get_workload`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
