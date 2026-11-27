# TaskService_update

**Entry point:** `task_service.TaskService.update`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [execution_planning_window](../modules/execution_planning_window.md), [models_task](../modules/models_task.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [snapshot_service](../modules/snapshot_service.md), [task_brief_service](../modules/task_brief_service.md), [task_domain_service](../modules/task_domain_service.md), [task_service](../modules/task_service.md)

> Update an existing task.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `execution_planning_window.current_window`
3. `execution_planning_window.execution_context`
4. `snapshot_service.SnapshotService`
5. `task_domain_service.require_owner`
6. `task_domain_service.normalize_effort`
7. `task_brief_service.render_brief`
8. `task_brief_service.TaskBriefService.apply_brief`
9. `task_brief_service.TaskBriefService`
10. `models_task.TaskDependency`
11. `execution_planning_window.is_planning_only_change`
12. `execution_planning_window.live_assignments`
13. `execution_planning_window.current_window`
14. `execution_planning_window.execution_context`
15. `task_brief_service.clear_execution_evidence`
16. `task_brief_service.clear_acceptance`
17. `execution_planning_window.fence_planning_only_edit`
18. `outbound_webhook_service.emit_outbound_webhook_event`
19. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [models_task](../modules/models_task.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_domain_service](../modules/task_domain_service.md)
- [task_service](../modules/task_service.md)

## Behavior

This workflow starts at `task_service.TaskService.update`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.

Backlog project changes require edit permission in both scopes. Project locks are acquired in ascending ID order and the task scope is rechecked before writing. The complete subtree must have no incoming or outgoing dependency across its boundary. Both backlogs receive transactional recovery points, descendants reserve one version per command, and rejected moves roll everything back. Actual dependency changes invalidate current progress and acceptance through general updates and individual add/remove commands. Immutable evidence history remains available, a command reserves one task version, and no-op dependency requests retain their current version. Locked graph relationships are loaded explicitly before applying a dependency update.
