# BacklogSnapshotService_restore

**Entry point:** `backlog_snapshot_service.BacklogSnapshotService.restore`
**Modules involved:** [authority](../modules/authority.md), [backlog_snapshot_service](../modules/backlog_snapshot_service.md), [commands](../modules/commands.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [models_task](../modules/models_task.md), [snapshot_service](../modules/snapshot_service.md), [task_brief_service](../modules/task_brief_service.md), [task_domain_service](../modules/task_domain_service.md), [task_recovery_service](../modules/task_recovery_service.md), [task_service](../modules/task_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `commands.lock_backlog_project`
3. `snapshot_service.SnapshotService._encode`
4. `task_service.TaskService`
5. `task_service.TaskService._load_iteration_tree`
6. `authority.AuthorityError`
7. `task_service.TaskService._require_unclaimed_structure`
8. `snapshot_service.SnapshotService._preflight_profile_lifetimes`
9. `snapshot_service.SnapshotService`
10. `authority.internal_authority`
11. `delivery_dependency_service.DeliveryDependencyService.require_unreferenced`
12. `delivery_dependency_service.DeliveryDependencyService`
13. `task_recovery_service.reserve_restored_task_version`
14. `models_task.Task`
15. `task_domain_service.require_owner`
16. `task_brief_service.TaskBriefService.restore_brief`
17. `task_brief_service.TaskBriefService`
18. `task_service.TaskService.record_task_event`
19. `models_task.TaskDependency`
20. `task_service.TaskService._load_iteration_tree`
21. `task_service.TaskService.task_to_response`

## Touches

- [authority](../modules/authority.md)
- [backlog_snapshot_service](../modules/backlog_snapshot_service.md)
- [commands](../modules/commands.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [models_task](../modules/models_task.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_domain_service](../modules/task_domain_service.md)
- [task_recovery_service](../modules/task_recovery_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `backlog_snapshot_service.BacklogSnapshotService.restore`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.

Scheduled and backlog restoration share a version allocator under the owning scope lock. It advances above the saved version, live task, retained history and durable deletion fence. Current progress and acceptance are cleared; immutable history survives. A deleted task without a reliable deletion fence returns snapshot_version_history_unknown (409), requiring recovery from a complete matching database backup.
