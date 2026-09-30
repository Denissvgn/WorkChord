# TaskService__lock_task_scope

**Entry point:** `task_service.TaskService._lock_task_scope`
**Modules involved:** [authority](../modules/authority.md), [backlog_snapshot_service](../modules/backlog_snapshot_service.md), [commands](../modules/commands.md), [task_service](../modules/task_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.lock_planning`
2. `authority.require_project`
3. `authority.require_project`
4. `commands.lock_backlog_project`
5. `authority.AuthorityError`
6. `backlog_snapshot_service.BacklogSnapshotService`
7. `commands.lock_iterations`

## Touches

- [authority](../modules/authority.md)
- [backlog_snapshot_service](../modules/backlog_snapshot_service.md)
- [commands](../modules/commands.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `task_service.TaskService._lock_task_scope`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.

Backlog project changes require edit permission in both scopes. Project locks are acquired in ascending ID order and the task scope is rechecked before writing. The complete subtree must have no incoming or outgoing dependency across its boundary. Both backlogs receive transactional recovery points, descendants reserve one version per command, and rejected moves roll everything back.
