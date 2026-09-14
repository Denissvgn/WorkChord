# assert_postgresql_contract

**Entry point:** `transfer._assert_postgresql_contract`
**Modules involved:** [catalog](../modules/catalog.md), [source](../modules/source.md), [transfer](../modules/transfer.md), [upgrade_service](../modules/upgrade_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `source.MigrationDataError`
2. `source.MigrationDataError`
3. `catalog.application_tables`
4. `source.MigrationDataError`
5. `upgrade_service.head_revision`
6. `source.MigrationDataError`
7. `source.MigrationDataError`
8. `source.MigrationDataError`
9. `source.MigrationDataError`

## Touches

- [catalog](../modules/catalog.md)
- [source](../modules/source.md)
- [transfer](../modules/transfer.md)
- [upgrade_service](../modules/upgrade_service.md)

## Behavior

This workflow starts at `transfer._assert_postgresql_contract`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
