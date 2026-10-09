# repair_sequences

**Entry point:** `transfer._repair_sequences`
**Modules involved:** [catalog](../modules/catalog.md), [project_identity](../modules/project_identity.md), [source](../modules/source.md), [transfer](../modules/transfer.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `catalog.transfer_order`
2. `catalog.transfer_tables`
3. `project_identity.project_allocation_floor`
4. `source.MigrationDataError`

## Touches

- [catalog](../modules/catalog.md)
- [project_identity](../modules/project_identity.md)
- [source](../modules/source.md)
- [transfer](../modules/transfer.md)

## Behavior

This workflow starts at `transfer._repair_sequences`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
