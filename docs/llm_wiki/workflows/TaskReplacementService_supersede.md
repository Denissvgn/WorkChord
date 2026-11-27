# TaskReplacementService_supersede

**Entry point:** `task_replacement_service.TaskReplacementService.supersede`
**Modules involved:** [commands](../modules/commands.md), [identity_service](../modules/identity_service.md), [models_task_replacement](../modules/models_task_replacement.md), [snapshot_service](../modules/snapshot_service.md), [task_reactivation_service](../modules/task_reactivation_service.md), [task_replacement_service](../modules/task_replacement_service.md), [time](../modules/time.md)

> Record that a closed or accepted successor already delivered this original's work.

Neither task is reopened or re-executed. The original keeps its status,
progress, attempts and history; unless it was already canceled it is
withdrawn as superseded work, so the deliverable counts once, through the
successor. Its dependents, delivery prerequisites, release membership and
open reactivation requirements move to the successor.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.lock_backlog_project`
2. `commands.PlanningConflict`
3. `snapshot_service.SnapshotService`
4. `task_reactivation_service.request_reactivation_check`
5. `identity_service.acting_principal_id`
6. `models_task_replacement.TaskReplacement`
7. `time.utc_now`
8. `time.utc_now`

## Touches

- [commands](../modules/commands.md)
- [identity_service](../modules/identity_service.md)
- [models_task_replacement](../modules/models_task_replacement.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_reactivation_service](../modules/task_reactivation_service.md)
- [task_replacement_service](../modules/task_replacement_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `task_replacement_service.TaskReplacementService.supersede`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
