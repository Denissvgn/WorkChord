# OutboundWebhookTarget

**Location:** `frontend/src/types/outboundWebhook.ts:3`
**Kind:** Class
**Bases:** —
**Module:** [outboundWebhook](../modules/outboundWebhook.md)

## Description

_Auto-generated from `OutboundWebhookTarget` in `frontend/src/types/outboundWebhook.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `number` | *required* | — |
| `name` | `string` | *required* | — |
| `description` | `string \| null` | *required* | — |
| `url` | `string` | *required* | — |
| `enabled` | `boolean` | *required* | — |
| `subscribed_events_json` | `string[]` | *required* | — |
| `has_secret` | `boolean` | *required* | — |
| `headers_json` | `Record<string, string>` | *required* | — |
| `created_at` | `string` | *required* | — |
| `updated_at` | `string` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["OutboundWebhookTarget (frontend/src/types/outboundWebhook.ts)"]
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
| [outboundWebhook](../modules/outboundWebhook.md) | 0 | `created_at`, `description`, `enabled`, `has_secret`, `headers_json`, `id`, `name`, `subscribed_events_json`, `updated_at`, `url` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `OutboundWebhooksPanel.test` | import | [OutboundWebhooksPanel.test](../modules/OutboundWebhooksPanel.test.md) | — |
| `OutboundWebhooksPanel` | import | [OutboundWebhooksPanel](../modules/OutboundWebhooksPanel.md) | — |
| `outboundWebhookService` | import | [outboundWebhookService](../modules/outboundWebhookService.md) | — |
