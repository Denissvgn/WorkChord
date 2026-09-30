# DiscussionService_retry

**Entry point:** `discussion_service.DiscussionService.retry`
**Modules involved:** [authority](../modules/authority.md), [commands](../modules/commands.md), [discussion_service](../modules/discussion_service.md), [time](../modules/time.md)

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `commands.PlanningConflict`
2. `authority.internal_authority`
3. `time.utc_now`

## Touches

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [discussion_service](../modules/discussion_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `discussion_service.DiscussionService.retry`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
