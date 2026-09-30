# TaskStatusService_change_status

**Entry point:** `task_status_service.TaskStatusService.change_status`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), [language_service](../modules/language_service.md), [snapshot_service](../modules/snapshot_service.md), [task_brief_service](../modules/task_brief_service.md), [task_status_service](../modules/task_status_service.md)

> Apply one valid direct transition and reconcile its ancestor chain.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.AuthorityError`
2. `authority.AuthorityError`
3. `authority.AuthorityError`
4. `authority.require_project`
5. `task_brief_service.TaskBriefService`
6. `language_service.resolve_runtime_ui_language`
7. `delivery_dependency_service.DeliveryDependencyService`
8. `language_service.task_requires_schedule_message`
9. `language_service.incomplete_dependency_message`
10. `snapshot_service.SnapshotService`
11. `task_brief_service.TaskBriefService`
12. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [language_service](../modules/language_service.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_status_service](../modules/task_status_service.md)

## Behavior

This workflow starts at `task_status_service.TaskStatusService.change_status`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
