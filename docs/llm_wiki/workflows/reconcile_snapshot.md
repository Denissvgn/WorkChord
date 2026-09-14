# reconcile_snapshot

**Entry point:** `transfer.reconcile_snapshot`
**Modules involved:** [database_migration_manifest](../modules/database_migration_manifest.md), [source](../modules/source.md), [time](../modules/time.md), [transfer](../modules/transfer.md), [upgrade_service](../modules/upgrade_service.md)

> Reconcile raw or post-repair target state and advance readiness safely.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `source.MigrationDataError`
2. `source.MigrationDataError`
3. `database_migration_manifest.read_document`
4. `source.MigrationDataError`
5. `source.MigrationDataError`
6. `source.MigrationDataError`
7. `source.MigrationDataError`
8. `source.MigrationDataError`
9. `time.utc_now`
10. `source.read_only_sqlite`
11. `upgrade_service.head_revision`
12. `database_migration_manifest.write_document`
13. `time.utc_now`
14. `source.MigrationDataError`

## Touches

- [database_migration_manifest](../modules/database_migration_manifest.md)
- [source](../modules/source.md)
- [time](../modules/time.md)
- [transfer](../modules/transfer.md)
- [upgrade_service](../modules/upgrade_service.md)

## Behavior

This workflow starts at `transfer.reconcile_snapshot`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
