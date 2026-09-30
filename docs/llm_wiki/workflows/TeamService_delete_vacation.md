# TeamService_delete_vacation

**Entry point:** `team_service.TeamService.delete_vacation`
**Modules involved:** [authority](../modules/authority.md), [capacity_service](../modules/capacity_service.md), [commands](../modules/commands.md), [team_service](../modules/team_service.md)

> Delete a vacation.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.internal_authority`
2. `capacity_service.CapacityService`
3. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [capacity_service](../modules/capacity_service.md)
- [commands](../modules/commands.md)
- [team_service](../modules/team_service.md)

## Behavior

This workflow starts at `team_service.TeamService.delete_vacation`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
