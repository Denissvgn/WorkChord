# InterfaceLanguageSettings Module

**Path:** `frontend/src/components/settings/InterfaceLanguageSettings.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/InterfaceLanguageSettings.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Select` | `Select` | — | compiler-dependent |
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
    n1["frontend/src/components/common/Select.tsx"]
    n2["frontend/src/components/feedback/QueryState.tsx"]
    n3["frontend/src/components/feedback/toast.ts"]
    n4["frontend/src/components/settings/InterfaceLanguageSettings.tsx"]
    n5["frontend/src/components/settings/SettingsUnsavedBar.tsx"]
    n6["frontend/src/i18n/i18n.ts"]
    n7["frontend/src/pages/SettingsPage.tsx"]
    n8["frontend/src/services/systemSettingsService.ts"]
    n9["frontend/src/types/systemSettings.ts"]
    n10["frontend/src/utils/adminAccess.ts"]
    n2 --> n0
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n4 --> n8
    n4 --> n9
    n4 --> n10
    n5 --> n0
    n7 --> n0
    n7 --> n4
    n8 --> n9
    click n0 "../modules/Button.md"
    click n1 "../modules/Select.md"
    click n2 "../modules/QueryState.md"
    click n3 "../modules/toast.md"
    click n4 "../modules/InterfaceLanguageSettings.md"
    click n5 "../modules/SettingsUnsavedBar.md"
    click n6 "../modules/i18n.md"
    click n7 "../modules/SettingsPage.md"
    click n8 "../modules/systemSettingsService.md"
    click n9 "../modules/systemSettings.md"
    click n10 "../modules/adminAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [SettingsPage](../modules/SettingsPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Select](../modules/Select.md) |
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
