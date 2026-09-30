# InterfaceLanguageSettings Module

**Path:** `frontend/src/components/settings/InterfaceLanguageSettings.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/InterfaceLanguageSettings.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../i18n/i18n` | `changeAppLanguage` |
| `../../services/systemSettingsService` | `systemSettingsService` |
| `../../types/systemSettings` | `AppRuntimeSettingsUpdate`, `LanguageCode`, `RuntimeSettingSource`, `SystemSettings` |
| `../../utils/adminAccess` | `getAdminAccessErrorMessage` |
| `../common/Button` | `Button` |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` |
| `../feedback/toast` | `useToast` |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` |
| `lucide-react` | `Globe2`, `Save` |
| `react` | `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `InterfaceLanguageSettings` |
| Constants | `sourceClass` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/components/feedback/toast.ts"]
    n3["frontend/src/components/settings/InterfaceLanguageSettings.tsx"]
    n4["frontend/src/i18n/i18n.ts"]
    n5["frontend/src/pages/SettingsPage.tsx"]
    n6["frontend/src/services/systemSettingsService.ts"]
    n7["frontend/src/types/systemSettings.ts"]
    n8["frontend/src/utils/adminAccess.ts"]
    n1 --> n0
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n5 --> n3
    n6 --> n7
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/toast.md"
    click n3 "../modules/InterfaceLanguageSettings.md"
    click n4 "../modules/i18n.md"
    click n5 "../modules/SettingsPage.md"
    click n6 "../modules/systemSettingsService.md"
    click n7 "../modules/systemSettings.md"
    click n8 "../modules/adminAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [SettingsPage](../modules/SettingsPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [toast](../modules/toast.md) |
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
