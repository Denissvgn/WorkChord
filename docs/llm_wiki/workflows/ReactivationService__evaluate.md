# ReactivationService__evaluate

**Entry point:** `task_reactivation_service.ReactivationService._evaluate`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [task_reactivation_service](../modules/task_reactivation_service.md), [time](../modules/time.md)

> Mark each requirement that now holds as met and reactivate once every one is met.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.utc_now`
2. `commands.lock_planning`
3. `authority.internal_authority`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [task_reactivation_service](../modules/task_reactivation_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `task_reactivation_service.ReactivationService._evaluate`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
