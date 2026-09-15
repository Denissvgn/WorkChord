# useAdminAccess Module

**Path:** `frontend/src/hooks/useAdminAccess.ts`

## Description

_Auto-generated from `frontend/src/hooks/useAdminAccess.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../features/identity/identityContext` | `useIdentity` |
| `../utils/adminAccess` | `ADMIN_API_KEY_CHANGED_EVENT`, `hasAdminApiKey` |
| `react` | `useEffect`, `useState` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `useAdminAccess` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/AdminAccessGate.tsx"]
    n1["frontend/src/components/settings/AdminAccessPanel.tsx"]
    n2["frontend/src/components/settings/EmailSettingsPanel.tsx"]
    n3["frontend/src/components/settings/OutboundWebhooksPanel.tsx"]
    n4["frontend/src/components/settings/RuntimeConfigSettings.tsx"]
    n5["frontend/src/components/settings/SchedulingRulesSettings.tsx"]
    n6["frontend/src/features/identity/identityContext.ts"]
    n7["frontend/src/hooks/useAdminAccess.ts"]
    n8["frontend/src/i18n/SystemLanguageProvider.tsx"]
    n9["frontend/src/pages/AgentPipelinePage.tsx"]
    n10["frontend/src/pages/SettingsPage.tsx"]
    n11["frontend/src/utils/adminAccess.ts"]
    n0 --> n1
    n0 --> n7
    n1 --> n7
    n1 --> n11
    n2 --> n7
    n2 --> n11
    n3 --> n7
    n3 --> n11
    n4 --> n7
    n4 --> n11
    n5 --> n7
    n5 --> n11
    n7 --> n6
    n7 --> n11
    n8 --> n7
    n9 --> n0
    n9 --> n7
    n10 --> n0
    n10 --> n1
    n10 --> n2
    n10 --> n3
    n10 --> n4
    n10 --> n5
    n10 --> n7
    click n0 "../modules/AdminAccessGate.md"
    click n1 "../modules/AdminAccessPanel.md"
    click n2 "../modules/EmailSettingsPanel.md"
    click n3 "../modules/OutboundWebhooksPanel.md"
    click n4 "../modules/RuntimeConfigSettings.md"
    click n5 "../modules/SchedulingRulesSettings.md"
    click n6 "../modules/identityContext.md"
    click n7 "../modules/useAdminAccess.md"
    click n8 "../modules/SystemLanguageProvider.md"
    click n9 "../modules/AgentPipelinePage.md"
    click n10 "../modules/SettingsPage.md"
    click n11 "../modules/adminAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AdminAccessGate](../modules/AdminAccessGate.md) |
| Inbound | [AdminAccessPanel](../modules/AdminAccessPanel.md) |
| Inbound | [EmailSettingsPanel](../modules/EmailSettingsPanel.md) |
| Inbound | [OutboundWebhooksPanel](../modules/OutboundWebhooksPanel.md) |
| Inbound | [RuntimeConfigSettings](../modules/RuntimeConfigSettings.md) |
| Inbound | [SchedulingRulesSettings](../modules/SchedulingRulesSettings.md) |
| Inbound | [SystemLanguageProvider](../modules/SystemLanguageProvider.md) |
| Inbound | [AgentPipelinePage](../modules/AgentPipelinePage.md) |
| Inbound | [SettingsPage](../modules/SettingsPage.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [adminAccess](../modules/adminAccess.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useAdminAccess` | `()` | — | — |
