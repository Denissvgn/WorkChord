# TeamService_add_vacation

**Entry point:** `team_service.TeamService.add_vacation`
**Modules involved:** [authority](../modules/authority.md), [capacity_service](../modules/capacity_service.md), [commands](../modules/commands.md), [team_member](../modules/team_member.md), [team_service](../modules/team_service.md)

> Add a vacation, optionally leaving commit ownership to the caller.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `team_member.Vacation`
2. `capacity_service.CapacityService`
3. `commands.commit_or_flush`
4. `authority.internal_authority`

## Touches

- [authority](../modules/authority.md)
- [capacity_service](../modules/capacity_service.md)
- [commands](../modules/commands.md)
- [team_member](../modules/team_member.md)
- [team_service](../modules/team_service.md)

## Behavior

This workflow starts at `team_service.TeamService.add_vacation`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
