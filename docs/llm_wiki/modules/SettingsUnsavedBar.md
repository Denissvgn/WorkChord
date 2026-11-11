# SettingsUnsavedBar Module

**Path:** `frontend/src/components/settings/SettingsUnsavedBar.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/SettingsUnsavedBar.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/UnsavedLeaveGuard` | `UnsavedLeaveGuard` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `SettingsUnsavedBar` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/UnsavedLeaveGuard.tsx"]
    n2["frontend/src/components/settings/EmailSettingsPanel.tsx"]
    n3["frontend/src/components/settings/GitHubSettingsPanel.tsx"]
    n4["frontend/src/components/settings/InterfaceLanguageSettings.tsx"]
    n5["frontend/src/components/settings/OutboundWebhooksPanel.tsx"]
    n6["frontend/src/components/settings/RuntimeConfigSettings.tsx"]
    n7["frontend/src/components/settings/SchedulingRulesSettings.tsx"]
    n8["frontend/src/components/settings/SettingsAccessAndAbout.test.tsx"]
    n9["frontend/src/components/settings/SettingsUnsavedBar.tsx"]
    n2 --> n0
    n2 --> n9
    n3 --> n0
    n3 --> n9
    n4 --> n0
    n4 --> n9
    n5 --> n0
    n5 --> n9
    n6 --> n0
    n6 --> n9
    n7 --> n0
    n7 --> n9
    n8 --> n9
    n9 --> n0
    n9 --> n1
    click n0 "../modules/Button.md"
    click n1 "../modules/UnsavedLeaveGuard.md"
    click n2 "../modules/EmailSettingsPanel.md"
    click n3 "../modules/GitHubSettingsPanel.md"
    click n4 "../modules/InterfaceLanguageSettings.md"
    click n5 "../modules/OutboundWebhooksPanel.md"
    click n6 "../modules/RuntimeConfigSettings.md"
    click n7 "../modules/SchedulingRulesSettings.md"
    click n8 "../modules/SettingsAccessAndAbout.test.md"
    click n9 "../modules/SettingsUnsavedBar.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [EmailSettingsPanel](../modules/EmailSettingsPanel.md) |
| Inbound | [GitHubSettingsPanel](../modules/GitHubSettingsPanel.md) |
| Inbound | [InterfaceLanguageSettings](../modules/InterfaceLanguageSettings.md) |
| Inbound | [OutboundWebhooksPanel](../modules/OutboundWebhooksPanel.md) |
| Inbound | [RuntimeConfigSettings](../modules/RuntimeConfigSettings.md) |
| Inbound | [SchedulingRulesSettings](../modules/SchedulingRulesSettings.md) |
| Inbound | [SettingsAccessAndAbout.test](../modules/SettingsAccessAndAbout.test.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [UnsavedLeaveGuard](../modules/UnsavedLeaveGuard.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `SettingsUnsavedBar` | <pre><code>&#40;&#123; dirty&#44; saving &#61; false&#44; onSave&#44; onDiscard&#44; hint &#125;&#58; &#123;&#10;    dirty&#58; boolean&#59; saving&#63;&#58; boolean&#59; onSave&#63;&#58; &#40;&#41; &#61;&#62; void&#59; onDiscard&#63;&#58; &#40;&#41; &#61;&#62; void&#59; hint&#63;&#58; string&#59;&#10;&#125;&#41;</code></pre> | — | Says a settings panel has unsaved changes, keeps Save and Discard in reach, |
