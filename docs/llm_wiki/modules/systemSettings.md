# systemSettings Module

**Path:** `frontend/src/types/systemSettings.ts`

## Description

_Auto-generated from `frontend/src/types/systemSettings.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AILanguageMode`, `AppRuntimeSettings`, `AppRuntimeSettingsUpdate`, `GitHubRuntimeSettings`, `GitHubRuntimeSettingsUpdate`, `LLMProvider`, `LLMRuntimeSettings`, `LLMRuntimeSettingsUpdate`, `LanguageCode`, `RestartRequiredSetting`, `RuntimeSettingSource`, `SystemSettings`, `WebIntakeRuntimeSettings`, `WebIntakeRuntimeSettingsUpdate` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/EmailSettingsPanel.tsx"]
    n1["frontend/src/components/settings/InterfaceLanguageSettings.tsx"]
    n2["frontend/src/components/settings/RuntimeConfigSettings.test.tsx"]
    n3["frontend/src/components/settings/RuntimeConfigSettings.tsx"]
    n4["frontend/src/services/systemSettingsService.ts"]
    n5["frontend/src/types/emailSettings.ts"]
    n6["frontend/src/types/systemSettings.ts"]
    n0 --> n5
    n0 --> n6
    n1 --> n4
    n1 --> n6
    n2 --> n3
    n2 --> n6
    n3 --> n4
    n3 --> n6
    n4 --> n6
    n5 --> n6
    click n0 "../modules/EmailSettingsPanel.md"
    click n1 "../modules/InterfaceLanguageSettings.md"
    click n2 "../modules/RuntimeConfigSettings.test.md"
    click n3 "../modules/RuntimeConfigSettings.md"
    click n4 "../modules/systemSettingsService.md"
    click n5 "../modules/emailSettings.md"
    click n6 "../modules/systemSettings.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [EmailSettingsPanel](../modules/EmailSettingsPanel.md) |
| Inbound | [InterfaceLanguageSettings](../modules/InterfaceLanguageSettings.md) |
| Inbound | [RuntimeConfigSettings.test](../modules/RuntimeConfigSettings.test.md) |
| Inbound | [RuntimeConfigSettings](../modules/RuntimeConfigSettings.md) |
| Inbound | [systemSettingsService](../modules/systemSettingsService.md) |
| Inbound | [emailSettings](../modules/emailSettings.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [AppRuntimeSettings](../entities/AppRuntimeSettings.md) | Class | 6 | — | — |
| [AppRuntimeSettingsUpdate](../entities/systemSettings_AppRuntimeSettingsUpdate.md) | Class | 12 | — | — |
| [LLMRuntimeSettings](../entities/LLMRuntimeSettings.md) | Class | 18 | — | — |
| [LLMRuntimeSettingsUpdate](../entities/systemSettings_LLMRuntimeSettingsUpdate.md) | Class | 28 | — | — |
| [GitHubRuntimeSettings](../entities/GitHubRuntimeSettings.md) | Class | 39 | — | — |
| [GitHubRuntimeSettingsUpdate](../entities/systemSettings_GitHubRuntimeSettingsUpdate.md) | Class | 48 | — | — |
| [WebIntakeRuntimeSettings](../entities/WebIntakeRuntimeSettings.md) | Class | 59 | — | — |
| [WebIntakeRuntimeSettingsUpdate](../entities/systemSettings_WebIntakeRuntimeSettingsUpdate.md) | Class | 65 | — | — |
| [RestartRequiredSetting](../entities/systemSettings_RestartRequiredSetting.md) | Class | 72 | — | — |
| [SystemSettings](../entities/SystemSettings.md) | Class | 77 | — | — |
| [RuntimeSettingSource](../entities/systemSettings_RuntimeSettingSource.md) | Type alias | 1 | — | — |
| [LLMProvider](../entities/systemSettings_LLMProvider.md) | Type alias | 2 | — | — |
| [LanguageCode](../entities/systemSettings_LanguageCode.md) | Type alias | 3 | — | — |
| [AILanguageMode](../entities/systemSettings_AILanguageMode.md) | Type alias | 4 | — | — |
