# CapacityTransferService__withdraw

**Entry point:** `capacity_transfers.CapacityTransferService._withdraw`
**Modules involved:** [capacity_adjustments](../modules/capacity_adjustments.md), [capacity_transfers](../modules/capacity_transfers.md), [commands](../modules/commands.md), [team_member](../modules/team_member.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.current_command`
2. `commands.PlanningConflict`
3. `commands.PlanningConflict`
4. `capacity_adjustments._days`
5. `time.utc_now`
6. `team_member.TeamMemberCapacityAdjustment`
7. `capacity_adjustments._days`

## Touches

- [capacity_adjustments](../modules/capacity_adjustments.md)
- [capacity_transfers](../modules/capacity_transfers.md)
- [commands](../modules/commands.md)
- [team_member](../modules/team_member.md)
- [time](../modules/time.md)

## Behavior

A temporary capacity transfer lends part of the availability of one or more source rows to a target row of the same person for a dated range. It is recorded as dated adjustments sharing one group token, so each source counts its own percentage minus the lent percentage and the target adds the lent total on those dates only; the prior shares return after the end date without a scheduled job and the rows' own percentages are never edited. Preview rolls everything back. Apply and withdraw are one shared planning input command over every row they change, so both sides change together or not at all, and an intervening change to an affected iteration is a revision conflict. No task, assignment or run changes, and a source reduction or target restoration on dates where that row's issued work is scheduled is refused.
