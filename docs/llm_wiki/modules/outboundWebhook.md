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
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/settings/OutboundWebhooksPanel.test.tsx"]
    n1["frontend/src/components/settings/OutboundWebhooksPanel.tsx"]
    n2["frontend/src/pages/SettingsPage.labels.test.tsx"]
    n3["frontend/src/pages/SettingsPage.readOnlyPanels.test.tsx"]
    n4["frontend/src/services/outboundWebhookService.ts"]
    n5["frontend/src/types/outboundWebhook.ts"]
    n0 --> n1
    n0 --> n5
    n1 --> n4
    n1 --> n5
    n2 --> n5
    n3 --> n5
    n4 --> n5
    click n0 "../modules/OutboundWebhooksPanel.test.md"
    click n1 "../modules/OutboundWebhooksPanel.md"
    click n2 "../modules/SettingsPage.labels.test.md"
    click n3 "../modules/SettingsPage.readOnlyPanels.test.md"
    click n4 "../modules/outboundWebhookService.md"
    click n5 "../modules/outboundWebhook.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [OutboundWebhooksPanel.test](../modules/OutboundWebhooksPanel.test.md) |
| Inbound | [OutboundWebhooksPanel](../modules/OutboundWebhooksPanel.md) |
| Inbound | [SettingsPage.labels.test](../modules/SettingsPage.labels.test.md) |
| Inbound | [SettingsPage.readOnlyPanels.test](../modules/SettingsPage.readOnlyPanels.test.md) |
| Inbound | [outboundWebhookService](../modules/outboundWebhookService.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [OutboundWebhookTarget](../entities/outboundWebhook_OutboundWebhookTarget.md) | Interface | 3 | — | — |
| [OutboundWebhookTargetCreate](../entities/outboundWebhook_OutboundWebhookTargetCreate.md) | Interface | 18 | — | — |
| [OutboundWebhookEvent](../entities/outboundWebhook_OutboundWebhookEvent.md) | Interface | 30 | — | — |
| [OutboundWebhookDelivery](../entities/outboundWebhook_OutboundWebhookDelivery.md) | Interface | 40 | — | — |
| [OutboundWebhookRetryResponse](../entities/outboundWebhook_OutboundWebhookRetryResponse.md) | Interface | 61 | — | — |
| [OutboundWebhookDeliveryListParams](../entities/OutboundWebhookDeliveryListParams.md) | Interface | 65 | — | — |
| [OutboundWebhookDeliveryStatus](../entities/outboundWebhook_OutboundWebhookDeliveryStatus.md) | Type alias | 1 | `'pending' \| 'delivered' \| 'failed'` | — |
| [OutboundWebhookTargetUpdate](../entities/outboundWebhook_OutboundWebhookTargetUpdate.md) | Type alias | 28 | `Partial<OutboundWebhookTargetCreate>` | — |
