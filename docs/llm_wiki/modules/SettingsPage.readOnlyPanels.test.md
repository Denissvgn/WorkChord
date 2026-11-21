# SettingsPage.readOnlyPanels.test Module

**Path:** `frontend/src/pages/SettingsPage.readOnlyPanels.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/SettingsPage.readOnlyPanels.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../features/identity/identityContext` | `IdentityContext` | — | compiler-dependent |
| `../features/identity/identityService` | `WorkspaceIdentity` | Declaration | erased |
| `../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../types/github` | `GitHubStatusAutomationRule` | Declaration | erased |
| `../types/label` | `LabelGroup` | Declaration | erased |
| `../types/outboundWebhook` | `OutboundWebhookTarget` | Declaration | erased |
| `../types/schedulingRules` | `SchedulingRulesResponse` | Declaration | erased |
| `../types/systemSettings` | `SystemSettings` | Declaration | erased |
| `../types/template` | `WorkTemplate` | Declaration | erased |
| `./SettingsPage` | `SettingsPage` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `within` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `templateServiceMock`, `labelServiceMock`, `rulesServiceMock`, `verifyKey`, `webhookServiceMock`, `githubServiceMock`, `systemSettingsServiceMock`, `labelGroup`, `rules`, `webhookTarget`, `githubRule`, `systemSettings`, `reader` |
| Module calls | `templateServiceMock = hoisted`, `labelServiceMock = hoisted`, `rulesServiceMock = hoisted`, `verifyKey = hoisted`, `mock`, `webhookServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `githubServiceMock = hoisted`, `systemSettingsServiceMock = hoisted`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/features/identity/identityContext.ts"]
    n1["frontend/src/features/identity/identityService.ts"]
    n2["frontend/src/pages/SettingsPage.readOnlyPanels.test.tsx"]
    n3["frontend/src/pages/SettingsPage.tsx"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n5["frontend/src/types/github.ts"]
    n6["frontend/src/types/label.ts"]
    n7["frontend/src/types/outboundWebhook.ts"]
    n8["frontend/src/types/schedulingRules.ts"]
    n9["frontend/src/types/systemSettings.ts"]
    n10["frontend/src/types/template.ts"]
    n0 --> n1
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n2 --> n8
    n2 --> n9
    n2 --> n10
    click n0 "../modules/identityContext.md"
    click n1 "../modules/identityService.md"
    click n2 "../modules/SettingsPage.readOnlyPanels.test.md"
    click n3 "../modules/SettingsPage.md"
    click n4 "../modules/renderWithProviders.md"
    click n5 "../modules/types_github.md"
    click n6 "../modules/types_label.md"
    click n7 "../modules/outboundWebhook.md"
    click n8 "../modules/schedulingRules.md"
    click n9 "../modules/systemSettings.md"
    click n10 "../modules/types_template.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [identityService](../modules/identityService.md) |
| Outbound | [SettingsPage](../modules/SettingsPage.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_github](../modules/types_github.md) |
| Outbound | [types_label](../modules/types_label.md) |
| Outbound | [outboundWebhook](../modules/outboundWebhook.md) |
| Outbound | [schedulingRules](../modules/schedulingRules.md) |
| Outbound | [systemSettings](../modules/systemSettings.md) |
| Outbound | [types_template](../modules/types_template.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
