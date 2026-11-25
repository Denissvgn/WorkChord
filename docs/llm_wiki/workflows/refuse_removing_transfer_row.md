# refuse_removing_transfer_row

**Entry point:** `capacity_transfers.refuse_removing_transfer_row`
**Modules involved:** [authority](../modules/authority.md), [capacity_transfers](../modules/capacity_transfers.md), [commands](../modules/commands.md), [services_work_metrics](../modules/services_work_metrics.md)

> Removing a row would leave the other rows of an unfinished transfer changed alone.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.internal_authority`
2. `services_work_metrics.working_today`
3. `commands.PlanningConflict`

## Touches

- [authority](../modules/authority.md)
- [capacity_transfers](../modules/capacity_transfers.md)
- [commands](../modules/commands.md)
- [services_work_metrics](../modules/services_work_metrics.md)

## Behavior

Refuses removing a capacity row that belongs to an unfinished transfer, because the other rows would stay changed alone.
