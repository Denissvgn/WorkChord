# OutboundWebhookDelivery

**Location:** `frontend/src/types/outboundWebhook.ts:38`
**Kind:** Class
**Bases:** —
**Module:** [outboundWebhook](../modules/outboundWebhook.md)

## Description

_Auto-generated from `OutboundWebhookDelivery` in `frontend/src/types/outboundWebhook.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `target_id` | `number \| null` | No | — | — |
| `event_id` | `number` | Yes | — | — |
| `target_name` | `string \| null` | No | — | — |
| `target_url` | `string \| null` | No | — | — |
| `status` | `OutboundWebhookDeliveryStatus` | Yes | — | — |
| `attempt_count` | `number` | Yes | — | — |
| `last_http_status` | `number \| null` | No | — | — |
| `last_error` | `string \| null` | No | — | — |
| `last_response_body` | `string \| null` | No | — | — |
| `last_attempt_at` | `string \| null` | No | — | — |
| `next_retry_at` | `string \| null` | No | — | — |
| `delivered_at` | `string \| null` | No | — | — |
| `created_at` | `string` | Yes | — | — |
| `updated_at` | `string` | Yes | — | — |
| `event` | `OutboundWebhookEvent` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["OutboundWebhookDelivery (frontend/src/types/outboundWebhook.ts)"]
    n1["frontend/src/components/settings/OutboundWebhooksPanel.test.tsx"]
    n2["frontend/src/components/settings/OutboundWebhooksPanel.tsx"]
    n3["frontend/src/services/outboundWebhookService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/outboundWebhook.md"
    click n1 "../modules/OutboundWebhooksPanel.test.md"
    click n2 "../modules/OutboundWebhooksPanel.md"
    click n3 "../modules/outboundWebhookService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [outboundWebhook](../modules/outboundWebhook.md) | 0 | `attempt_count`, `created_at`, `delivered_at`, `event`, `event_id`, `id`, `last_attempt_at`, `last_error`, `last_http_status`, `last_response_body`, `next_retry_at`, `status` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `OutboundWebhooksPanel.test` | import | [OutboundWebhooksPanel.test](../modules/OutboundWebhooksPanel.test.md) | — |
| `OutboundWebhooksPanel` | import | [OutboundWebhooksPanel](../modules/OutboundWebhooksPanel.md) | — |
| `outboundWebhookService` | import | [outboundWebhookService](../modules/outboundWebhookService.md) | — |
