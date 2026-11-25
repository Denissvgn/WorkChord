# TaskReplacementService_record

**Entry point:** `task_replacement_service.TaskReplacementService.record`
**Modules involved:** [commands](../modules/commands.md), [identity_service](../modules/identity_service.md), [models_task_replacement](../modules/models_task_replacement.md), [snapshot_service](../modules/snapshot_service.md), [task_brief_service](../modules/task_brief_service.md), [task_replacement_service](../modules/task_replacement_service.md), [time](../modules/time.md)

> Link a fresh replacement to an unaccepted original under one audited decision.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.lock_backlog_project`
2. `commands.PlanningConflict`
3. `commands.PlanningConflict`
4. `snapshot_service.SnapshotService`
5. `identity_service.acting_principal_id`
6. `models_task_replacement.TaskReplacement`
7. `time.utc_now`
8. `time.utc_now`
9. `task_brief_service.clear_acceptance`

## Touches

- [commands](../modules/commands.md)
- [identity_service](../modules/identity_service.md)
- [models_task_replacement](../modules/models_task_replacement.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_replacement_service](../modules/task_replacement_service.md)
- [time](../modules/time.md)

## Behavior

Records an audited clean replacement of task work that cannot be attributed. Deciding needs manage permission on the project; an agent caller must also be the project's PM or an operator. The original must be an unaccepted leaf task with no live assignment, running run or claim; the replacement must be a fresh planned leaf task of the same project and milestone with no attempts, assignments or acceptance, and neither may already take part in a replacement. Carried runs must be recorded contributions of the original. In one command it snapshots the iteration, moves schedule and delivery dependents and open release membership to the replacement, cancels the original with the reason and keeps its attempts and unknown attribution. The original is then never reviewed, and a replacement that carries commits from an unattributed run stays held.
