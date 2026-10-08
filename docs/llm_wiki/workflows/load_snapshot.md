# load_snapshot

**Entry point:** `transfer.load_snapshot`
**Modules involved:** [catalog](../modules/catalog.md), [config](../modules/config.md), [database_migration_manifest](../modules/database_migration_manifest.md), [project_identity](../modules/project_identity.md), [source](../modules/source.md), [time](../modules/time.md), [transfer](../modules/transfer.md)

> Load a catalogued snapshot into an empty, Alembic-current target.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `source.MigrationDataError`
2. `project_identity.sqlite_project_allocation_floor`
3. `config.get_settings`
4. `source.MigrationDataError`
5. `database_migration_manifest.write_document`
6. `time.utc_now`
7. `source.read_only_sqlite`
8. `catalog.transfer_order`
9. `catalog.transfer_tables`
10. `source.MigrationDataError`
11. `source.MigrationDataError`
12. `time.utc_now`
13. `catalog.transfer_order`
14. `catalog.transfer_tables`
15. `catalog.transfer_order`
16. `time.utc_now`
17. `source._file_sha256`
18. `source.MigrationDataError`
19. `database_migration_manifest.write_document`
20. `source.MigrationDataError`
21. `source.MigrationDataError`

## Touches

- [catalog](../modules/catalog.md)
- [config](../modules/config.md)
- [database_migration_manifest](../modules/database_migration_manifest.md)
- [project_identity](../modules/project_identity.md)
- [source](../modules/source.md)
- [time](../modules/time.md)
- [transfer](../modules/transfer.md)

## Behavior

This workflow starts at `transfer.load_snapshot`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
