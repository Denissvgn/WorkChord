# PlanShareService_create

**Entry point:** `plan_share_service.PlanShareService.create`
**Modules involved:** [models_plan_share](../modules/models_plan_share.md), [plan_share_service](../modules/plan_share_service.md), [snapshot_service](../modules/snapshot_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `snapshot_service.SnapshotService`
2. `time.utc_now`
3. `models_plan_share.PlanShare`

## Touches

- [models_plan_share](../modules/models_plan_share.md)
- [plan_share_service](../modules/plan_share_service.md)
- [snapshot_service](../modules/snapshot_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `plan_share_service.PlanShareService.create`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
