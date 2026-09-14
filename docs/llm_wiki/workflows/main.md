# main

**Entry point:** `database_migration.main`
**Modules involved:** [cli_database_migration](../modules/cli_database_migration.md), [source](../modules/source.md), [transfer](../modules/transfer.md), [upgrade_service](../modules/upgrade_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `source.preflight_source`
2. `upgrade_service.database_configuration`
3. `source.MigrationDataError`
4. `transfer.target_identifier`
5. `transfer.load_snapshot`
6. `transfer.record_post_copy_repairs`
7. `transfer.reconcile_snapshot`

## Touches

- [cli_database_migration](../modules/cli_database_migration.md)
- [source](../modules/source.md)
- [transfer](../modules/transfer.md)
- [upgrade_service](../modules/upgrade_service.md)

## Behavior

This workflow starts at `database_migration.main`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
