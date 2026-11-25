# CapacityAdjustmentService__change

**Entry point:** `capacity_adjustments.CapacityAdjustmentService._change`
**Modules involved:** [capacity_adjustments](../modules/capacity_adjustments.md), [capacity_service](../modules/capacity_service.md), [capacity_transfers](../modules/capacity_transfers.md), [commands](../modules/commands.md), [models_identity](../modules/models_identity.md), [team_member](../modules/team_member.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.current_command`
2. `commands.PlanningConflict`
3. `commands.PlanningConflict`
4. `capacity_transfers.refuse_withdrawing_transfer_side`
5. `commands.PlanningConflict`
6. `commands.PlanningConflict`
7. `commands.PlanningConflict`
8. `commands.PlanningConflict`
9. `commands.PlanningConflict`
10. `capacity_service.CapacityService`
11. `capacity_service.CapacityService.coverage_for`
12. `capacity_service.CapacityService.absence_ranges`
13. `time.utc_now`
14. `team_member.TeamMemberCapacityAdjustment`
15. `models_identity.CommandAudit`

## Touches

- [capacity_adjustments](../modules/capacity_adjustments.md)
- [capacity_service](../modules/capacity_service.md)
- [capacity_transfers](../modules/capacity_transfers.md)
- [commands](../modules/commands.md)
- [models_identity](../modules/models_identity.md)
- [team_member](../modules/team_member.md)
- [time](../modules/time.md)

## Behavior

A dated capacity adjustment replaces one capacity row's availability percentage on a bounded date range only; every other date keeps the row's own value. Preview runs the real change inside a rolled-back command and returns the effective daily capacity with the change; apply records it under the observed planning revisions. A change advances the shared planning revision and the revision of each affected iteration, changes no task version and leaves issued work current. A reduction on dates where the row's issued work is scheduled is refused, and a row without an iteration cannot be adjusted.
