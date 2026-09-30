# OutboundWebhookService__attempt_delivery

**Entry point:** `outbound_webhook_service.OutboundWebhookService._attempt_delivery`
**Modules involved:** [commands](../modules/commands.md), [discussion_service](../modules/discussion_service.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [time](../modules/time.md)

> Attempt one claimed delivery and persist success, retry, or terminal state.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.as_utc`
2. `time.utc_now`
3. `discussion_service.DiscussionService`
4. `commands.commit_or_flush`

## Touches

- [commands](../modules/commands.md)
- [discussion_service](../modules/discussion_service.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `outbound_webhook_service.OutboundWebhookService._attempt_delivery`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
