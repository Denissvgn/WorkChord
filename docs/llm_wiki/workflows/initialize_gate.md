# initialize_gate

**Entry point:** `transfer._initialize_gate`
**Modules involved:** [catalog](../modules/catalog.md), [source](../modules/source.md), [time](../modules/time.md), [transfer](../modules/transfer.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `source.MigrationDataError`
2. `source.MigrationDataError`
3. `catalog.transfer_tables`
4. `source.MigrationDataError`
5. `time.utc_now`
6. `time.utc_now`

## Touches

- [catalog](../modules/catalog.md)
- [source](../modules/source.md)
- [time](../modules/time.md)
- [transfer](../modules/transfer.md)

## Behavior

This workflow starts at `transfer._initialize_gate`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
