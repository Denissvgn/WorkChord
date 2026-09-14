# load_source_manifest

**Entry point:** `transfer._load_source_manifest`
**Modules involved:** [catalog](../modules/catalog.md), [database_migration_manifest](../modules/database_migration_manifest.md), [source](../modules/source.md), [transfer](../modules/transfer.md), [upgrade_service](../modules/upgrade_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `database_migration_manifest.read_document`
2. `source.MigrationDataError`
3. `source.MigrationDataError`
4. `source.MigrationDataError`
5. `source.MigrationDataError`
6. `upgrade_service.head_revision`
7. `source.MigrationDataError`
8. `source._file_sha256`
9. `source.MigrationDataError`
10. `catalog.catalog_entries`
11. `source.MigrationDataError`
12. `catalog.transfer_order`
13. `source.MigrationDataError`
14. `source.read_only_sqlite`
15. `source._inspect_snapshot`
16. `source.MigrationDataError`

## Touches

- [catalog](../modules/catalog.md)
- [database_migration_manifest](../modules/database_migration_manifest.md)
- [source](../modules/source.md)
- [transfer](../modules/transfer.md)
- [upgrade_service](../modules/upgrade_service.md)

## Behavior

This workflow starts at `transfer._load_source_manifest`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
