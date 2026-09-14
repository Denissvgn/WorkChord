# load_snapshot

**Entry point:** `transfer.load_snapshot`
**Modules involved:** [catalog](../modules/catalog.md), [config](../modules/config.md), [database_migration_manifest](../modules/database_migration_manifest.md), [source](../modules/source.md), [time](../modules/time.md), [transfer](../modules/transfer.md)

> Load a catalogued snapshot into an empty, Alembic-current target.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `source.MigrationDataError`
2. `config.get_settings`
3. `source.MigrationDataError`
4. `database_migration_manifest.write_document`
5. `time.utc_now`
6. `source.read_only_sqlite`
7. `catalog.transfer_order`
8. `catalog.transfer_tables`
9. `source.MigrationDataError`
10. `source.MigrationDataError`
11. `time.utc_now`
12. `catalog.transfer_order`
13. `catalog.transfer_tables`
14. `catalog.transfer_order`
15. `time.utc_now`
16. `source._file_sha256`
17. `source.MigrationDataError`
18. `database_migration_manifest.write_document`
19. `source.MigrationDataError`
20. `source.MigrationDataError`

## Touches

- [catalog](../modules/catalog.md)
- [config](../modules/config.md)
- [database_migration_manifest](../modules/database_migration_manifest.md)
- [source](../modules/source.md)
- [time](../modules/time.md)
- [transfer](../modules/transfer.md)

## Behavior

This workflow starts at `transfer.load_snapshot`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
