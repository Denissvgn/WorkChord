# reconcile_snapshot

**Entry point:** `transfer.reconcile_snapshot`
**Modules involved:** [database_migration_manifest](../modules/database_migration_manifest.md), [project_identity](../modules/project_identity.md), [source](../modules/source.md), [time](../modules/time.md), [transfer](../modules/transfer.md), [upgrade_service](../modules/upgrade_service.md)

> Reconcile raw or post-repair target state and advance readiness safely.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `source.MigrationDataError`
2. `project_identity.sqlite_project_allocation_floor`
3. `source.MigrationDataError`
4. `database_migration_manifest.read_document`
5. `source.MigrationDataError`
6. `source.MigrationDataError`
7. `source.MigrationDataError`
8. `source.MigrationDataError`
9. `source.MigrationDataError`
10. `time.utc_now`
11. `source.read_only_sqlite`
12. `upgrade_service.head_revision`
13. `database_migration_manifest.write_document`
14. `time.utc_now`
15. `source.MigrationDataError`

## Touches

- [database_migration_manifest](../modules/database_migration_manifest.md)
- [project_identity](../modules/project_identity.md)
- [source](../modules/source.md)
- [time](../modules/time.md)
- [transfer](../modules/transfer.md)
- [upgrade_service](../modules/upgrade_service.md)

## Behavior

This workflow starts at `transfer.reconcile_snapshot`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
