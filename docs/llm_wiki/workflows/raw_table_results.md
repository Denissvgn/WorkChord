# raw_table_results

**Entry point:** `transfer._raw_table_results`
**Modules involved:** [catalog](../modules/catalog.md), [database_migration_canonical](../modules/database_migration_canonical.md), [source](../modules/source.md), [transfer](../modules/transfer.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `catalog.transfer_order`
2. `catalog.transfer_tables`
3. `database_migration_canonical.digest_rows`
4. `source._rows`
5. `database_migration_canonical.digest_rows`
6. `source._rows`
7. `database_migration_canonical.canonical_value`
8. `database_migration_canonical.canonical_value`
9. `source.MigrationDataError`

## Touches

- [catalog](../modules/catalog.md)
- [database_migration_canonical](../modules/database_migration_canonical.md)
- [source](../modules/source.md)
- [transfer](../modules/transfer.md)

## Behavior

This workflow starts at `transfer._raw_table_results`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
