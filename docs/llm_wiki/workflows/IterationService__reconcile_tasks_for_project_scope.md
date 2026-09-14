# IterationService__reconcile_tasks_for_project_scope

**Entry point:** `iteration_service.IterationService._reconcile_tasks_for_project_scope`
**Modules involved:** [iteration_service](../modules/iteration_service.md), [query_limits](../modules/query_limits.md), [snapshot_service](../modules/snapshot_service.md), [task_service](../modules/task_service.md)

> Apply or validate task project links when iteration scope changes.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `query_limits.CollectionLimitExceededError`
2. `snapshot_service.SnapshotService`
3. `task_service.TaskService`

## Touches

- [iteration_service](../modules/iteration_service.md)
- [query_limits](../modules/query_limits.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `iteration_service.IterationService._reconcile_tasks_for_project_scope`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
