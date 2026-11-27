# TaskPostponementService_resume

**Entry point:** `task_postponement_service.TaskPostponementService.resume`
**Modules involved:** [identity_service](../modules/identity_service.md), [task_postponement_service](../modules/task_postponement_service.md), [task_reactivation_service](../modules/task_reactivation_service.md), [time](../modules/time.md)

> Move locked postponed work back to planned or resolved and close its postponement.

An automatic resume is the server's own decision once the recorded
requirements hold: it names no person and its audit rows are written as
the system. Work postponed without a record (an imported file, for
example) returns to planned.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.utc_now`
2. `identity_service.acting_principal_id`
3. `task_reactivation_service.request_reactivation_check`

## Touches

- [identity_service](../modules/identity_service.md)
- [task_postponement_service](../modules/task_postponement_service.md)
- [task_reactivation_service](../modules/task_reactivation_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `task_postponement_service.TaskPostponementService.resume`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
