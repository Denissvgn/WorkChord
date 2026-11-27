# ReactivationService_record_owner_decision

**Entry point:** `task_reactivation_service.ReactivationService.record_owner_decision`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [task_postponement_service](../modules/task_postponement_service.md), [task_reactivation_service](../modules/task_reactivation_service.md), [time](../modules/time.md)

> The owner's command: record that the decision an owner_decision requirement waits for was made.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `commands.lock_planning`
3. `authority.internal_authority`
4. `task_postponement_service.open_postponement`
5. `commands.PlanningConflict`
6. `time.utc_now`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [task_postponement_service](../modules/task_postponement_service.md)
- [task_reactivation_service](../modules/task_reactivation_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `task_reactivation_service.ReactivationService.record_owner_decision`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
