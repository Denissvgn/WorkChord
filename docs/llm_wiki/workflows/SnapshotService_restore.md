# SnapshotService_restore

**Entry point:** `snapshot_service.SnapshotService.restore`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [config](../modules/config.md), [models_task](../modules/models_task.md), [recovery](../modules/recovery.md), [snapshot_service](../modules/snapshot_service.md), [snapshots](../modules/snapshots.md), [task_service](../modules/task_service.md), [team_member](../modules/team_member.md)

> Restore supported IDs in place, retain history and invalidate current execution acceptance.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `authority.require_operator`
3. `commands.lock_iterations`
4. `task_service.TaskService`
5. `snapshots._validate_snapshot_task_payloads`
6. `team_member.TeamMember`
7. `team_member.Vacation`
8. `models_task.Task`
9. `recovery.TaskScheduleBaseline`
10. `models_task.TaskDependency`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [models_task](../modules/models_task.md)
- [recovery](../modules/recovery.md)
- [snapshot_service](../modules/snapshot_service.md)
- [snapshots](../modules/snapshots.md)
- [task_service](../modules/task_service.md)
- [team_member](../modules/team_member.md)

## Behavior

This workflow starts at `snapshot_service.SnapshotService.restore`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
