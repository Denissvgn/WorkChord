# TeamService_calculate_capacity

**Entry point:** `team_service.TeamService.calculate_capacity`
**Modules involved:** [calendar_service](../modules/calendar_service.md), [capacity_service](../modules/capacity_service.md), [schemas_team](../modules/schemas_team.md), [team_service](../modules/team_service.md)

> Calculate capacity for a team member.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `capacity_service.CapacityService`
2. `calendar_service.CalendarService`
3. `capacity_service.day_hours`
4. `schemas_team.MemberCapacity`

## Touches

- [calendar_service](../modules/calendar_service.md)
- [capacity_service](../modules/capacity_service.md)
- [schemas_team](../modules/schemas_team.md)
- [team_service](../modules/team_service.md)

## Behavior

This workflow starts at `team_service.TeamService.calculate_capacity`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
