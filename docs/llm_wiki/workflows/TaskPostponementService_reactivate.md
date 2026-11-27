# TaskPostponementService_reactivate

**Entry point:** `task_postponement_service.TaskPostponementService.reactivate`
**Modules involved:** [commands](../modules/commands.md), [identity_service](../modules/identity_service.md), [task_postponement_service](../modules/task_postponement_service.md), [time](../modules/time.md)

> Return postponed work to planned, or to resolved if it was postponed after resolution.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.PlanningConflict`
2. `time.utc_now`
3. `identity_service.acting_principal_id`

## Touches

- [commands](../modules/commands.md)
- [identity_service](../modules/identity_service.md)
- [task_postponement_service](../modules/task_postponement_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `task_postponement_service.TaskPostponementService.reactivate`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
