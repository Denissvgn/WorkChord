# SystemSettings

**Location:** `frontend/src/types/systemSettings.ts:77`
**Kind:** Interface
**Bases:** —
**Module:** [systemSettings](../modules/systemSettings.md)

## Description

_Auto-generated from `SystemSettings` in `frontend/src/types/systemSettings.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `app` | `AppRuntimeSettings` | Yes | — | — |
| `llm` | `LLMRuntimeSettings` | Yes | — | — |
| `github` | `GitHubRuntimeSettings` | Yes | — | — |
| `web_intake` | `WebIntakeRuntimeSettings` | Yes | — | — |
| `restart_required` | `RestartRequiredSetting[]` | Yes | — | — |
| `redacted_fields` | `string[]` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SystemSettings (frontend/src/types/systemSettings.ts)"]
    n1["frontend/src/components/settings/InterfaceLanguageSettings.tsx"]
    n2["frontend/src/components/settings/RuntimeConfigSettings.test.tsx"]
    n3["frontend/src/components/settings/RuntimeConfigSettings.tsx"]
    n4["frontend/src/pages/SettingsPage.labels.test.tsx"]
    n5["frontend/src/pages/SettingsPage.readOnlyPanels.test.tsx"]
    n6["frontend/src/services/systemSettingsService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/systemSettings.md"
    click n1 "../modules/InterfaceLanguageSettings.md"
    click n2 "../modules/RuntimeConfigSettings.test.md"
    click n3 "../modules/RuntimeConfigSettings.md"
    click n4 "../modules/SettingsPage.labels.test.md"
    click n5 "../modules/SettingsPage.readOnlyPanels.test.md"
    click n6 "../modules/systemSettingsService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [systemSettings](../modules/systemSettings.md) | 0 | `app`, `github`, `llm`, `redacted_fields`, `restart_required`, `web_intake` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `InterfaceLanguageSettings` | import | [InterfaceLanguageSettings](../modules/InterfaceLanguageSettings.md) | — |
| `RuntimeConfigSettings.test` | import | [RuntimeConfigSettings.test](../modules/RuntimeConfigSettings.test.md) | — |
| `RuntimeConfigSettings` | import | [RuntimeConfigSettings](../modules/RuntimeConfigSettings.md) | — |
| `SettingsPage.labels.test` | import | [SettingsPage.labels.test](../modules/SettingsPage.labels.test.md) | — |
| `SettingsPage.readOnlyPanels.test` | import | [SettingsPage.readOnlyPanels.test](../modules/SettingsPage.readOnlyPanels.test.md) | — |
| `systemSettingsService` | import | [systemSettingsService](../modules/systemSettingsService.md) | — |
