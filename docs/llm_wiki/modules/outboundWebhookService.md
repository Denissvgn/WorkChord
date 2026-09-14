# outboundWebhookService Module

**Path:** `frontend/src/services/outboundWebhookService.ts`

## Description

_Auto-generated from `frontend/src/services/outboundWebhookService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/outboundWebhook` | `OutboundWebhookDelivery`, `OutboundWebhookDeliveryListParams`, `OutboundWebhookRetryResponse`, `OutboundWebhookTarget`, `OutboundWebhookTargetCreate`, `OutboundWebhookTargetUpdate` |
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `outboundWebhookService` |
| Constants | `outboundWebhookService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/OutboundWebhooksPanel.tsx"]
    n1["frontend/src/services/api.ts"]
    n2["frontend/src/services/outboundWebhookService.ts"]
    n3["frontend/src/types/outboundWebhook.ts"]
    n0 --> n2
    n0 --> n3
    n2 --> n1
    n2 --> n3
    click n0 "../modules/OutboundWebhooksPanel.md"
    click n1 "../modules/api.md"
    click n2 "../modules/outboundWebhookService.md"
    click n3 "../modules/outboundWebhook.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [OutboundWebhooksPanel](../modules/OutboundWebhooksPanel.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [outboundWebhook](../modules/outboundWebhook.md) |
