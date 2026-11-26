# TaskService_unmerge_task

**Entry point:** `task_service.TaskService.unmerge_task`
**Modules involved:** [authority](../modules/authority.md), [snapshot_service](../modules/snapshot_service.md), [task_postponement_service](../modules/task_postponement_service.md), [task_service](../modules/task_service.md)

> Promote children into the parent's sibling scope without losing referenced work.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `snapshot_service.SnapshotService`
3. `task_postponement_service.require_unreferenced`

## Touches

- [authority](../modules/authority.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_postponement_service](../modules/task_postponement_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `task_service.TaskService.unmerge_task`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
