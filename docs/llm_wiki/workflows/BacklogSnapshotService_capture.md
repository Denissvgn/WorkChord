# BacklogSnapshotService_capture

**Entry point:** `backlog_snapshot_service.BacklogSnapshotService.capture`
**Modules involved:** [authority](../modules/authority.md), [backlog_snapshot_service](../modules/backlog_snapshot_service.md), [commands](../modules/commands.md), [config](../modules/config.md), [recovery](../modules/recovery.md), [snapshot_service](../modules/snapshot_service.md), [task_service](../modules/task_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `commands.current_command`
3. `commands.lock_backlog_project`
4. `task_service.TaskService._load_iteration_tree`
5. `task_service.TaskService`
6. `snapshot_service.SnapshotService`
7. `snapshot_service.SnapshotService._validate_reason`
8. `time.utc_now`
9. `snapshot_service.SnapshotService._task_to_export`
10. `snapshot_service.SnapshotService.profile_lifetimes`
11. `recovery.ApplicationSnapshot`
12. `config.get_settings`

## Touches

- [authority](../modules/authority.md)
- [backlog_snapshot_service](../modules/backlog_snapshot_service.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [recovery](../modules/recovery.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `backlog_snapshot_service.BacklogSnapshotService.capture`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
