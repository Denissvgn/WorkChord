# restore_staged_references

**Entry point:** `transfer._restore_staged_references`
**Modules involved:** [catalog](../modules/catalog.md), [database_migration_canonical](../modules/database_migration_canonical.md), [source](../modules/source.md), [transfer](../modules/transfer.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `catalog.staged_reference_columns`
2. `source._rows`
3. `database_migration_canonical.storage_value`
4. `database_migration_canonical.storage_value`

## Touches

- [catalog](../modules/catalog.md)
- [database_migration_canonical](../modules/database_migration_canonical.md)
- [source](../modules/source.md)
- [transfer](../modules/transfer.md)

## Behavior

This workflow starts at `transfer._restore_staged_references`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
