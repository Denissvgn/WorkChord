# TaskDomainService__cancel_execution

**Entry point:** `task_domain_service.TaskDomainService._cancel_execution`
**Modules involved:** [authority](../modules/authority.md), [review_provenance](../modules/review_provenance.md), [task_domain_service](../modules/task_domain_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.AuthorityError`
2. `review_provenance.different_publisher_required`
3. `review_provenance.mark_server_interruption`
4. `review_provenance.record_server_end_profile`
5. `time.utc_now`

## Touches

- [authority](../modules/authority.md)
- [review_provenance](../modules/review_provenance.md)
- [task_domain_service](../modules/task_domain_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `task_domain_service.TaskDomainService._cancel_execution`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
