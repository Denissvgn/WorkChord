# verify_action_lease

**Entry point:** `leases.verify_action_lease`
**Modules involved:** [autonomy_canonical](../modules/autonomy_canonical.md), [evidence](../modules/evidence.md), [leases](../modules/leases.md), [signing](../modules/signing.md)

> Adapter-side verification before any provider mutation.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `signing.verify_detached_signature`
2. `autonomy_canonical.canonical_json_bytes`
3. `evidence.validate_attempt_ledger_snapshot`

## Touches

- [autonomy_canonical](../modules/autonomy_canonical.md)
- [evidence](../modules/evidence.md)
- [leases](../modules/leases.md)
- [signing](../modules/signing.md)

## Behavior

This workflow starts at `leases.verify_action_lease`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
