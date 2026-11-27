# select_reviewer

**Entry point:** `review_provenance.select_reviewer`
**Modules involved:** [manual_provenance_service](../modules/manual_provenance_service.md), [review_provenance](../modules/review_provenance.md), [services_review_evidence](../modules/services_review_evidence.md), [task_replacement_service](../modules/task_replacement_service.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `task_replacement_service.attributed`
2. `manual_provenance_service.remedy`
3. `services_review_evidence.resolve`

## Touches

- [manual_provenance_service](../modules/manual_provenance_service.md)
- [review_provenance](../modules/review_provenance.md)
- [services_review_evidence](../modules/services_review_evidence.md)
- [task_replacement_service](../modules/task_replacement_service.md)

## Behavior

This workflow starts at `review_provenance.select_reviewer`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
