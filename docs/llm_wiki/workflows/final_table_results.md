# final_table_results

**Entry point:** `transfer._final_table_results`
**Modules involved:** [catalog](../modules/catalog.md), [database_migration_canonical](../modules/database_migration_canonical.md), [source](../modules/source.md), [transfer](../modules/transfer.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `source.MigrationDataError`
2. `catalog.transfer_order`
3. `catalog.transfer_tables`
4. `database_migration_canonical.digest_rows`
5. `source._rows`
6. `database_migration_canonical.digest_rows`
7. `source.MigrationDataError`
8. `source.MigrationDataError`

## Touches

- [catalog](../modules/catalog.md)
- [database_migration_canonical](../modules/database_migration_canonical.md)
- [source](../modules/source.md)
- [transfer](../modules/transfer.md)

## Behavior

This workflow starts at `transfer._final_table_results`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
