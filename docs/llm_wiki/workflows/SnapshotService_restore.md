# SnapshotService_restore

**Entry point:** `snapshot_service.SnapshotService.restore`
**Modules involved:** [authority](../modules/authority.md), [calendar_service](../modules/calendar_service.md), [capacity_adjustments](../modules/capacity_adjustments.md), [commands](../modules/commands.md), [config](../modules/config.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [models_task](../modules/models_task.md), [recovery](../modules/recovery.md), [snapshot_service](../modules/snapshot_service.md), [snapshots](../modules/snapshots.md), [task_brief_service](../modules/task_brief_service.md), [task_domain_service](../modules/task_domain_service.md), [task_recovery_service](../modules/task_recovery_service.md), [task_replacement_service](../modules/task_replacement_service.md), [task_service](../modules/task_service.md), [team_member](../modules/team_member.md), [team_service](../modules/team_service.md)

> Restore supported IDs in place, retain history and invalidate current execution acceptance.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `config.get_settings`
2. `authority.require_operator`
3. `commands.lock_iterations`
4. `task_service.TaskService`
5. `snapshots._validate_snapshot_task_payloads`
6. `task_service.TaskService.get_all_tasks`
7. `task_service.TaskService._require_unclaimed_structure`
8. `calendar_service.CalendarService`
9. `calendar_service.CalendarService.get_by_id`
10. `calendar_service.CalendarService.selected_years`
11. `team_member.TeamMember`
12. `team_service.TeamService.detach_absence_adapters`
13. `team_service.TeamService`
14. `capacity_adjustments.restore_adjustments`
15. `team_member.Vacation`
16. `task_replacement_service.require_restore_compatible`
17. `delivery_dependency_service.DeliveryDependencyService.require_unreferenced`
18. `delivery_dependency_service.DeliveryDependencyService`
19. `task_recovery_service.reserve_restored_task_version`
20. `models_task.Task`
21. `task_domain_service.require_owner`
22. `task_brief_service.TaskBriefService.restore_brief`
23. `task_brief_service.TaskBriefService`
24. `recovery.TaskScheduleBaseline`
25. `task_service.TaskService.record_task_event`
26. `models_task.TaskDependency`
27. `task_service.TaskService.record_task_event`

## Touches

- [authority](../modules/authority.md)
- [calendar_service](../modules/calendar_service.md)
- [capacity_adjustments](../modules/capacity_adjustments.md)
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
- [task_replacement_service](../modules/task_replacement_service.md)
- [task_service](../modules/task_service.md)
- [team_member](../modules/team_member.md)
- [team_service](../modules/team_service.md)

## Behavior

This workflow starts at `snapshot_service.SnapshotService.restore`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.

Scheduled and backlog restoration share a version allocator under the owning scope lock. It advances above the saved version, live task, retained history and durable deletion fence. Current progress and acceptance are cleared; immutable history survives. A deleted task without a reliable deletion fence returns snapshot_version_history_unknown (409), requiring recovery from a complete matching database backup.
