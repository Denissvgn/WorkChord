# TaskImportService_import_tasks

**Entry point:** `task_import_service.TaskImportService.import_tasks`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [import_parser](../modules/import_parser.md), [snapshot_service](../modules/snapshot_service.md), [task_domain_service](../modules/task_domain_service.md), [task_import_service](../modules/task_import_service.md)

> Import task text into executable tasks, triage items, or both by policy.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.require_project`
2. `commands.lock_iterations`
3. `snapshot_service.SnapshotService`
4. `import_parser.parse_tasks_text`
5. `task_domain_service.nominal_day_hours`
6. `commands.commit_or_flush`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [import_parser](../modules/import_parser.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_domain_service](../modules/task_domain_service.md)
- [task_import_service](../modules/task_import_service.md)

## Behavior

This workflow starts at `task_import_service.TaskImportService.import_tasks`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
