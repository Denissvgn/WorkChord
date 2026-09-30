# DiscussionService_deliver

**Entry point:** `discussion_service.DiscussionService.deliver`
**Modules involved:** [authority](../modules/authority.md), [discussion_service](../modules/discussion_service.md), [models_discussion](../modules/models_discussion.md), [outbound_webhook_service](../modules/outbound_webhook_service.md)

> Idempotent local inbox sink; no external recipient messaging occurs here.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `authority.internal_authority`
2. `outbound_webhook_service.OutboundDeliveryAttemptError`
3. `outbound_webhook_service.OutboundDeliveryAttemptError`
4. `models_discussion.InboxNotification`

## Touches

- [authority](../modules/authority.md)
- [discussion_service](../modules/discussion_service.md)
- [models_discussion](../modules/models_discussion.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)

## Behavior

This workflow starts at `discussion_service.DiscussionService.deliver`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
