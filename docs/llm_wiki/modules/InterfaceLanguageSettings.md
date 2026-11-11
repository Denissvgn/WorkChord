# InterfaceLanguageSettings Module

**Path:** `frontend/src/components/settings/InterfaceLanguageSettings.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/InterfaceLanguageSettings.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/i18n` | `changeAppLanguage` | — | compiler-dependent |
| `../../services/systemSettingsService` | `systemSettingsService` | — | compiler-dependent |
| `../../types/systemSettings` | `AppRuntimeSettingsUpdate`, `LanguageCode`, `RuntimeSettingSource`, `SystemSettings` | Declaration | erased |
| `../../utils/adminAccess` | `getAdminAccessErrorMessage` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `../feedback/toast` | `useToast` | — | compiler-dependent |
| `./SettingsUnsavedBar` | `SettingsUnsavedBar` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `lucide-react` | `Globe2`, `Save` | — | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `InterfaceLanguageSettings` |
| Constants | `sourceClass` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/components/feedback/toast.ts"]
    n3["frontend/src/components/settings/InterfaceLanguageSettings.tsx"]
    n4["frontend/src/components/settings/SettingsUnsavedBar.tsx"]
    n5["frontend/src/i18n/i18n.ts"]
    n6["frontend/src/pages/SettingsPage.tsx"]
    n7["frontend/src/services/systemSettingsService.ts"]
    n8["frontend/src/types/systemSettings.ts"]
    n9["frontend/src/utils/adminAccess.ts"]
    n1 --> n0
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n3 --> n7
    n3 --> n8
    n3 --> n9
    n4 --> n0
    n6 --> n3
    n7 --> n8
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/toast.md"
    click n3 "../modules/InterfaceLanguageSettings.md"
    click n4 "../modules/SettingsUnsavedBar.md"
    click n5 "../modules/i18n.md"
    click n6 "../modules/SettingsPage.md"
    click n7 "../modules/systemSettingsService.md"
    click n8 "../modules/systemSettings.md"
    click n9 "../modules/adminAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [SettingsPage](../modules/SettingsPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [toast](../modules/toast.md) |
| Outbound | [SettingsUnsavedBar](../modules/SettingsUnsavedBar.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [systemSettingsService](../modules/systemSettingsService.md) |
| Outbound | [systemSettings](../modules/systemSettings.md) |
| Outbound | [adminAccess](../modules/adminAccess.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `InterfaceLanguageSettings` | `()` | — | — |
