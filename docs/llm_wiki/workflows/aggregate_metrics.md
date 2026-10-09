# aggregate_metrics

**Entry point:** `work_metrics.aggregate_metrics`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [services_work_metrics](../modules/services_work_metrics.md), [time](../modules/time.md)

> Aggregate all authorized leaves in SQL, including inherited scheduling facets.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.utc_now`
2. `authority._scope_conditions`
3. `commands.HierarchyScopeError`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `work_metrics.aggregate_metrics`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
