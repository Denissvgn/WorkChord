# TaskImportService_bulk_update_tasks_from_text

**Entry point:** `task_import_service.TaskImportService.bulk_update_tasks_from_text`
**Modules involved:** [commands](../modules/commands.md), [import_parser](../modules/import_parser.md), [snapshot_service](../modules/snapshot_service.md), [task_import_service](../modules/task_import_service.md)

> Update ID-tagged tasks and create new tasks or triage items from text.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `snapshot_service.SnapshotService`
2. `import_parser.parse_tasks_text`
3. `commands.commit_or_flush`

## Touches

- [commands](../modules/commands.md)
- [import_parser](../modules/import_parser.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_import_service](../modules/task_import_service.md)

## Behavior

This workflow starts at `task_import_service.TaskImportService.bulk_update_tasks_from_text`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
