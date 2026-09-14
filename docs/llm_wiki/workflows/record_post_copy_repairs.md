# record_post_copy_repairs

**Entry point:** `transfer.record_post_copy_repairs`
**Modules involved:** [catalog](../modules/catalog.md), [database_migration_canonical](../modules/database_migration_canonical.md), [database_migration_manifest](../modules/database_migration_manifest.md), [source](../modules/source.md), [transfer](../modules/transfer.md), [upgrade_service](../modules/upgrade_service.md)

> Run the versioned repair catalog and record its exact row-hash delta.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `database_migration_manifest.read_document`
2. `source.MigrationDataError`
3. `source.MigrationDataError`
4. `source.MigrationDataError`
5. `source.MigrationDataError`
6. `catalog.transfer_tables`
7. `database_migration_canonical.digest_rows`
8. `upgrade_service.run_database_repairs`
9. `catalog.transfer_tables`
10. `source.MigrationDataError`
11. `database_migration_canonical.digest_rows`
12. `source.MigrationDataError`
13. `database_migration_manifest.write_document`
14. `source.MigrationDataError`

## Touches

- [catalog](../modules/catalog.md)
- [database_migration_canonical](../modules/database_migration_canonical.md)
- [database_migration_manifest](../modules/database_migration_manifest.md)
- [source](../modules/source.md)
- [transfer](../modules/transfer.md)
- [upgrade_service](../modules/upgrade_service.md)

## Behavior

This workflow starts at `transfer.record_post_copy_repairs`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
