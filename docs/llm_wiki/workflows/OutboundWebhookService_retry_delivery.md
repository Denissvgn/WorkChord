# OutboundWebhookService_retry_delivery

**Entry point:** `outbound_webhook_service.OutboundWebhookService.retry_delivery`
**Modules involved:** [commands](../modules/commands.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [schemas_outbound_webhook](../modules/schemas_outbound_webhook.md), [time](../modules/time.md)

> Request and immediately process one manual outbound retry.

## Sequence

<!-- Auto-generated static call-chain projection. Reviewed runtime ordering, branching, and side effects belong in Behavior. -->
1. `time.utc_now`
2. `commands.commit_or_flush`
3. `time.utc_now`
4. `schemas_outbound_webhook.OutboundWebhookRetryResponse`

## Touches

- [commands](../modules/commands.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [schemas_outbound_webhook](../modules/schemas_outbound_webhook.md)
- [time](../modules/time.md)

## Behavior

This workflow starts at `outbound_webhook_service.OutboundWebhookService.retry_delivery`. The generated sequence is a bounded static projection; runtime ordering, branching, and side effects require source-level confirmation.
