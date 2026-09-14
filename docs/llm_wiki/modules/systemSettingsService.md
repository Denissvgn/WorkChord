# systemSettingsService Module

**Path:** `frontend/src/services/systemSettingsService.ts`

## Description

_Auto-generated from `frontend/src/services/systemSettingsService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/systemSettings` | `AppRuntimeSettings`, `AppRuntimeSettingsUpdate`, `GitHubRuntimeSettings`, `GitHubRuntimeSettingsUpdate`, `LLMRuntimeSettings`, `LLMRuntimeSettingsUpdate`, `SystemSettings`, `WebIntakeRuntimeSettings`, `WebIntakeRuntimeSettingsUpdate` |
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `systemSettingsService` |
| Constants | `systemSettingsService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/InterfaceLanguageSettings.tsx"]
    n1["frontend/src/components/settings/RuntimeConfigSettings.tsx"]
    n2["frontend/src/i18n/SystemLanguageProvider.tsx"]
    n3["frontend/src/services/api.ts"]
    n4["frontend/src/services/systemSettingsService.ts"]
    n5["frontend/src/types/systemSettings.ts"]
    n0 --> n4
    n0 --> n5
    n1 --> n4
    n1 --> n5
    n2 --> n4
    n4 --> n3
    n4 --> n5
    click n0 "../modules/InterfaceLanguageSettings.md"
    click n1 "../modules/RuntimeConfigSettings.md"
    click n2 "../modules/SystemLanguageProvider.md"
    click n3 "../modules/api.md"
    click n4 "../modules/systemSettingsService.md"
    click n5 "../modules/systemSettings.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [InterfaceLanguageSettings](../modules/InterfaceLanguageSettings.md) |
| Inbound | [RuntimeConfigSettings](../modules/RuntimeConfigSettings.md) |
| Inbound | [SystemLanguageProvider](../modules/SystemLanguageProvider.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [systemSettings](../modules/systemSettings.md) |
