# LLMRuntimeSettings

**Location:** `frontend/src/types/systemSettings.ts:18`
**Kind:** Class
**Bases:** —
**Module:** [systemSettings](../modules/systemSettings.md)

## Description

_Auto-generated from `LLMRuntimeSettings` in `frontend/src/types/systemSettings.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `provider` | `LLMProvider` | *required* | — |
| `api_url` | `string` | *required* | — |
| `model` | `string` | *required* | — |
| `temperature` | `number` | *required* | — |
| `max_output_tokens` | `number` | *required* | — |
| `has_api_key` | `boolean` | *required* | — |
| `field_sources` | `Record<string, RuntimeSettingSource>` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["LLMRuntimeSettings (frontend/src/types/systemSettings.ts)"]
    n1["frontend/src/services/systemSettingsService.ts"]
    n1 --> n0
    click n0 "../modules/systemSettings.md"
    click n1 "../modules/systemSettingsService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [systemSettings](../modules/systemSettings.md) | 0 | `api_url`, `field_sources`, `has_api_key`, `max_output_tokens`, `model`, `provider`, `temperature` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `systemSettingsService` | import | [systemSettingsService](../modules/systemSettingsService.md) | — |
