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
7. `authority.require_project`
8. `task_brief_service.TaskBriefService`
9. `language_service.resolve_runtime_ui_language`
10. `delivery_dependency_service.DeliveryDependencyService`
11. `language_service.task_requires_schedule_message`
12. `language_service.incomplete_dependency_message`
13. `snapshot_service.SnapshotService`
14. `task_brief_service.TaskBriefService`
15. `commands.commit_or_flush`

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
