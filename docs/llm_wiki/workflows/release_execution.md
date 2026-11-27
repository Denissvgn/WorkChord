# release_execution

**Entry point:** `task_domain_service.release_execution`
**Modules involved:** [authority](../modules/authority.md), [review_provenance](../modules/review_provenance.md), [task_domain_service](../modules/task_domain_service.md), [time](../modules/time.md)

> End a task's claim, live assignments and running runs under the caller's ownership fence.

The caller holds the task's scope lock. When anything is live, the caller must
supply the current claim generation and the exact running run and live
assignment IDs, so ownership that changed after the caller read it is never
ended blind. Each affected agent's queue revision advances, and each run ends
with its server-recorded profile. The release is recorded as ``event_type``.
With ``only_when_live`` nothing is changed or recorded when nothing is live,
and None is returned; otherwise the released IDs are returned.

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

This workflow starts at `task_domain_service.release_execution`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
