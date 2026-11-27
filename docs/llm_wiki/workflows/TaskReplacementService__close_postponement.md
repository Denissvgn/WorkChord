# TaskReplacementService__close_postponement

**Entry point:** `task_replacement_service.TaskReplacementService._close_postponement`
**Modules involved:** [identity_service](../modules/identity_service.md), [task_postponement_service](../modules/task_postponement_service.md), [task_replacement_service](../modules/task_replacement_service.md), [time](../modules/time.md)

> End a postponed original's open postponement: its work is delivered, so nothing is left to wait for.

The postponement closes the way reactivation would, returning the original
to planned (or resolved, if it was postponed after resolution) under the
trigger ``supersession``; the original is then withdrawn as superseded, so
it never returns to work. Returns the closed postponement, or None when
the original was not postponed.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `task_postponement_service.open_postponement`
2. `task_postponement_service.reactivation_status`
3. `time.utc_now`
4. `identity_service.acting_principal_id`

## Touches

- [identity_service](../modules/identity_service.md)
- [task_postponement_service](../modules/task_postponement_service.md)
- [task_replacement_service](../modules/task_replacement_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `task_replacement_service.TaskReplacementService._close_postponement`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
