# outboundWebhook Module

**Path:** `frontend/src/types/outboundWebhook.ts`

## Description

_Auto-generated from `frontend/src/types/outboundWebhook.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `OutboundWebhookDelivery`, `OutboundWebhookDeliveryListParams`, `OutboundWebhookDeliveryStatus`, `OutboundWebhookEvent`, `OutboundWebhookRetryResponse`, `OutboundWebhookTarget`, `OutboundWebhookTargetCreate`, `OutboundWebhookTargetUpdate` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/OutboundWebhooksPanel.test.tsx"]
    n1["frontend/src/components/settings/OutboundWebhooksPanel.tsx"]
    n2["frontend/src/services/outboundWebhookService.ts"]
    n3["frontend/src/types/outboundWebhook.ts"]
    n0 --> n1
    n0 --> n3
    n1 --> n2
    n1 --> n3
    n2 --> n3
    click n0 "../modules/OutboundWebhooksPanel.test.md"
    click n1 "../modules/OutboundWebhooksPanel.md"
    click n2 "../modules/outboundWebhookService.md"
    click n3 "../modules/outboundWebhook.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [OutboundWebhooksPanel.test](../modules/OutboundWebhooksPanel.test.md) |
| Inbound | [OutboundWebhooksPanel](../modules/OutboundWebhooksPanel.md) |
| Inbound | [outboundWebhookService](../modules/outboundWebhookService.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [OutboundWebhookTarget](../entities/outboundWebhook_OutboundWebhookTarget.md) | Class | 3 | — | — |
| [OutboundWebhookTargetCreate](../entities/outboundWebhook_OutboundWebhookTargetCreate.md) | Class | 16 | — | — |
| [OutboundWebhookEvent](../entities/outboundWebhook_OutboundWebhookEvent.md) | Class | 28 | — | — |
| [OutboundWebhookDelivery](../entities/outboundWebhook_OutboundWebhookDelivery.md) | Class | 38 | — | — |
| [OutboundWebhookRetryResponse](../entities/outboundWebhook_OutboundWebhookRetryResponse.md) | Class | 57 | — | — |
| [OutboundWebhookDeliveryListParams](../entities/OutboundWebhookDeliveryListParams.md) | Class | 61 | — | — |
| [OutboundWebhookDeliveryStatus](../entities/outboundWebhook_OutboundWebhookDeliveryStatus.md) | Type alias | 1 | — | — |
| [OutboundWebhookTargetUpdate](../entities/outboundWebhook_OutboundWebhookTargetUpdate.md) | Type alias | 26 | — | — |
