# TaskImportService_bulk_update_tasks_from_text

**Entry point:** `task_import_service.TaskImportService.bulk_update_tasks_from_text`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [import_parser](../modules/import_parser.md), [schemas_task](../modules/schemas_task.md), [snapshot_service](../modules/snapshot_service.md), [task_domain_service](../modules/task_domain_service.md), [task_import_service](../modules/task_import_service.md)

> Update ID-tagged tasks and create new tasks or triage items from text.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `commands.lock_iterations`
3. `snapshot_service.SnapshotService`
4. `import_parser.parse_tasks_text`
5. `schemas_task.TaskUpdate`
6. `task_domain_service.nominal_day_hours`
7. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [import_parser](../modules/import_parser.md)
- [schemas_task](../modules/schemas_task.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_domain_service](../modules/task_domain_service.md)
- [task_import_service](../modules/task_import_service.md)

## Behavior

This workflow starts at `task_import_service.TaskImportService.bulk_update_tasks_from_text`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
