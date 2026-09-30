# SnapshotService_restore

**Entry point:** `snapshot_service.SnapshotService.restore`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [config](../modules/config.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [models_task](../modules/models_task.md), [recovery](../modules/recovery.md), [snapshot_service](../modules/snapshot_service.md), [snapshots](../modules/snapshots.md), [task_brief_service](../modules/task_brief_service.md), [task_domain_service](../modules/task_domain_service.md), [task_recovery_service](../modules/task_recovery_service.md), [task_service](../modules/task_service.md), [team_member](../modules/team_member.md), [team_service](../modules/team_service.md)

> Restore supported IDs in place, retain history and invalidate current execution acceptance.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `authority.require_operator`
3. `commands.lock_iterations`
4. `task_service.TaskService`
5. `snapshots._validate_snapshot_task_payloads`
6. `team_member.TeamMember`
7. `team_service.TeamService`
8. `team_member.Vacation`
9. `delivery_dependency_service.DeliveryDependencyService`
10. `task_recovery_service.reserve_restored_task_version`
11. `models_task.Task`
12. `task_domain_service.require_owner`
13. `task_brief_service.TaskBriefService`
14. `recovery.TaskScheduleBaseline`
15. `models_task.TaskDependency`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [models_task](../modules/models_task.md)
- [recovery](../modules/recovery.md)
- [snapshot_service](../modules/snapshot_service.md)
- [snapshots](../modules/snapshots.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_domain_service](../modules/task_domain_service.md)
- [task_recovery_service](../modules/task_recovery_service.md)
- [task_service](../modules/task_service.md)
- [team_member](../modules/team_member.md)
- [team_service](../modules/team_service.md)

## Behavior

This workflow starts at `snapshot_service.SnapshotService.restore`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.

Scheduled and backlog restoration share a version allocator under the owning scope lock. It advances above the saved version, live task, retained history and durable deletion fence. Current progress and acceptance are cleared; immutable history survives. A deleted task without a reliable deletion fence returns snapshot_version_history_unknown (409), requiring recovery from a complete matching database backup.
