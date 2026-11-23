# retained_witness

**Entry point:** `retained_planning_output._retained_witness`
**Modules involved:** [authority](../modules/authority.md), [execution_planning_window](../modules/execution_planning_window.md), [planning_window_reconciliation](../modules/planning_window_reconciliation.md), [retained_planning_output](../modules/retained_planning_output.md), [review_provenance](../modules/review_provenance.md), [time](../modules/time.md)

> Verify the shared public facts before giving queue guidance or recording the owner's statement.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `planning_window_reconciliation.source_receipt_id`
2. `planning_window_reconciliation.source_receipt_id`
3. `planning_window_reconciliation._planning_proof`
4. `authority.internal_authority`
5. `execution_planning_window.authority_stamp`
6. `review_provenance.actor_provenance`
7. `review_provenance.rework_binding_identity`
8. `review_provenance.rework_binding_identity`
9. `time.as_utc`
10. `time.as_utc`
11. `time.as_utc`
12. `time.as_utc`
13. `time.as_utc`
14. `time.as_utc`

## Touches

- [authority](../modules/authority.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [planning_window_reconciliation](../modules/planning_window_reconciliation.md)
- [retained_planning_output](../modules/retained_planning_output.md)
- [review_provenance](../modules/review_provenance.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `retained_planning_output._retained_witness`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
