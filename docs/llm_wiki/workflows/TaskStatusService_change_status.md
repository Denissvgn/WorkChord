# TaskStatusService_change_status

**Entry point:** `task_status_service.TaskStatusService.change_status`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [language_service](../modules/language_service.md), [services_work_metrics](../modules/services_work_metrics.md), [snapshot_service](../modules/snapshot_service.md), [task_brief_service](../modules/task_brief_service.md), [task_status_service](../modules/task_status_service.md)

> Apply one valid direct transition and reconcile its ancestor chain.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.AuthorityError`
2. `authority.AuthorityError`
3. `commands.PlanningConflict`
4. `authority.AuthorityError`
5. `services_work_metrics.effective_work_flags`
6. `commands.PlanningConflict`
7. `commands.current_command`
8. `authority.require_project`
9. `task_brief_service.TaskBriefService.require_review`
10. `task_brief_service.TaskBriefService`
11. `language_service.resolve_runtime_ui_language`
12. `delivery_dependency_service.DeliveryDependencyService.ready`
13. `delivery_dependency_service.DeliveryDependencyService`
14. `language_service.task_requires_schedule_message`
15. `language_service.incomplete_dependency_message`
16. `snapshot_service.SnapshotService`
17. `task_brief_service.TaskBriefService.record_review`
18. `task_brief_service.TaskBriefService`
19. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [language_service](../modules/language_service.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_status_service](../modules/task_status_service.md)

## Behavior

This workflow starts at `task_status_service.TaskStatusService.change_status`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
