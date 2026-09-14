# adminAccess Module

**Path:** `frontend/src/utils/adminAccess.ts`

## Description

_Auto-generated from `frontend/src/utils/adminAccess.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./apiError` | `getApiErrorMessage`, `getApiErrorStatus` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ADMIN_API_KEY_CHANGED_EVENT`, `ADMIN_API_KEY_STORAGE_KEY`, `AdminAccessErrorMessages`, `clearAdminApiKey`, `getAdminAccessErrorMessage`, `getAdminApiKey`, `hasAdminApiKey`, `setAdminApiKey` |
| Constants | `ADMIN_API_KEY_STORAGE_KEY`, `ADMIN_API_KEY_CHANGED_EVENT` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/AdminAccessPanel.tsx"]
    n1["frontend/src/components/settings/EmailSettingsPanel.tsx"]
    n2["frontend/src/components/settings/InterfaceLanguageSettings.tsx"]
    n3["frontend/src/components/settings/OutboundWebhooksPanel.tsx"]
    n4["frontend/src/components/settings/RuntimeConfigSettings.tsx"]
    n5["frontend/src/components/settings/SchedulingRulesSettings.tsx"]
    n6["frontend/src/hooks/useAdminAccess.ts"]
    n7["frontend/src/pages/GanttPage.tsx"]
    n8["frontend/src/pages/SettingsPage.test.tsx"]
    n9["frontend/src/services/api.ts"]
    n10["frontend/src/utils/adminAccess.ts"]
    n11["frontend/src/utils/apiError.ts"]
    n0 --> n6
    n0 --> n10
    n1 --> n6
    n1 --> n10
    n2 --> n10
    n3 --> n6
    n3 --> n10
    n4 --> n6
    n4 --> n10
    n5 --> n6
    n5 --> n10
    n6 --> n10
    n7 --> n10
    n7 --> n11
    n8 --> n10
    n9 --> n10
    n10 --> n11
    click n0 "../modules/AdminAccessPanel.md"
    click n1 "../modules/EmailSettingsPanel.md"
    click n2 "../modules/InterfaceLanguageSettings.md"
    click n3 "../modules/OutboundWebhooksPanel.md"
    click n4 "../modules/RuntimeConfigSettings.md"
    click n5 "../modules/SchedulingRulesSettings.md"
    click n6 "../modules/useAdminAccess.md"
    click n7 "../modules/GanttPage.md"
    click n8 "../modules/SettingsPage.test.md"
    click n9 "../modules/api.md"
    click n10 "../modules/adminAccess.md"
    click n11 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AdminAccessPanel](../modules/AdminAccessPanel.md) |
| Inbound | [EmailSettingsPanel](../modules/EmailSettingsPanel.md) |
| Inbound | [InterfaceLanguageSettings](../modules/InterfaceLanguageSettings.md) |
| Inbound | [OutboundWebhooksPanel](../modules/OutboundWebhooksPanel.md) |
| Inbound | [RuntimeConfigSettings](../modules/RuntimeConfigSettings.md) |
| Inbound | [SchedulingRulesSettings](../modules/SchedulingRulesSettings.md) |
| Inbound | [useAdminAccess](../modules/useAdminAccess.md) |
| Inbound | [GanttPage](../modules/GanttPage.md) |
| Inbound | [SettingsPage.test](../modules/SettingsPage.test.md) |
| Inbound | [api](../modules/api.md) |
| Outbound | [apiError](../modules/apiError.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [AdminAccessErrorMessages](../entities/AdminAccessErrorMessages.md) | Class | 6 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `getAdminApiKey` | `()` | — | — |
| `hasAdminApiKey` | `()` | — | — |
| `setAdminApiKey` | `(apiKey: string)` | — | — |
| `clearAdminApiKey` | `()` | — | — |
| `getAdminAccessErrorMessage` | `(error: unknown, messages: AdminAccessErrorMessages)` | — | — |
