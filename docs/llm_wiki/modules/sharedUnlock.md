# sharedUnlock Module

**Path:** `frontend/src/components/settings/sharedUnlock.ts`

## Description

_Auto-generated from `frontend/src/components/settings/sharedUnlock.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `react` | `createContext`, `useContext` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `SettingsReadOnly`, `SettingsReadOnlyContext`, `SharedUnlock`, `SharedUnlockContext`, `useSettingsReadOnly`, `useSharedUnlock` |
| Constants | `SharedUnlockContext`, `SettingsReadOnlyContext` |
| Module calls | `SharedUnlockContext = createContext`, `SettingsReadOnlyContext = createContext` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/AdminAccessGate.tsx"]
    n1["frontend/src/components/settings/GitHubSettingsPanel.tsx"]
    n2["frontend/src/components/settings/OutboundWebhooksPanel.tsx"]
    n3["frontend/src/components/settings/ReadOnlyFieldset.tsx"]
    n4["frontend/src/components/settings/SchedulingRulesSettings.tsx"]
    n5["frontend/src/components/settings/sharedUnlock.ts"]
    n6["frontend/src/components/settings/TemplateLabelSettings.tsx"]
    n7["frontend/src/components/team/ConnectAgentSteps.tsx"]
    n8["frontend/src/pages/SettingsPage.tsx"]
    n0 --> n5
    n1 --> n0
    n1 --> n5
    n2 --> n5
    n3 --> n5
    n4 --> n3
    n4 --> n5
    n6 --> n5
    n7 --> n5
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n8 --> n3
    n8 --> n4
    n8 --> n5
    n8 --> n6
    click n0 "../modules/AdminAccessGate.md"
    click n1 "../modules/GitHubSettingsPanel.md"
    click n2 "../modules/OutboundWebhooksPanel.md"
    click n3 "../modules/ReadOnlyFieldset.md"
    click n4 "../modules/SchedulingRulesSettings.md"
    click n5 "../modules/sharedUnlock.md"
    click n6 "../modules/TemplateLabelSettings.md"
    click n7 "../modules/ConnectAgentSteps.md"
    click n8 "../modules/SettingsPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AdminAccessGate](../modules/AdminAccessGate.md) |
| Inbound | [GitHubSettingsPanel](../modules/GitHubSettingsPanel.md) |
| Inbound | [OutboundWebhooksPanel](../modules/OutboundWebhooksPanel.md) |
| Inbound | [ReadOnlyFieldset](../modules/ReadOnlyFieldset.md) |
| Inbound | [SchedulingRulesSettings](../modules/SchedulingRulesSettings.md) |
| Inbound | [TemplateLabelSettings](../modules/TemplateLabelSettings.md) |
| Inbound | [ConnectAgentSteps](../modules/ConnectAgentSteps.md) |
| Inbound | [SettingsPage](../modules/SettingsPage.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [SharedUnlock](../entities/SharedUnlock.md) | Interface | 8 | — | Set by a page that shows one Unlock editing control for all of its protected |
| [SettingsReadOnly](../entities/SettingsReadOnly.md) | Interface | 22 | — | Set by a gate around content that disables its own editing controls while |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useSharedUnlock` | `()` | — | — |
| `useSettingsReadOnly` | `()` | — | Null when the content may be edited. |
