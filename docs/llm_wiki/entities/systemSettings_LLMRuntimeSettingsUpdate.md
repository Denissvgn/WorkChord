# LLMRuntimeSettingsUpdate

**Location:** `frontend/src/types/systemSettings.ts:28`
**Kind:** Class
**Bases:** —
**Module:** [systemSettings](../modules/systemSettings.md)

## Description

_Auto-generated from `LLMRuntimeSettingsUpdate` in `frontend/src/types/systemSettings.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `provider` | `LLMProvider` | No | — | — |
| `api_url` | `string` | No | — | — |
| `model` | `string` | No | — | — |
| `temperature` | `number` | No | — | — |
| `max_output_tokens` | `number` | No | — | — |
| `api_key` | `string \| null` | No | — | — |
| `clear_api_key` | `boolean` | No | — | — |
| `reset_fields` | `string[]` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["LLMRuntimeSettingsUpdate (frontend/src/types/systemSettings.ts)"]
    n1["frontend/src/components/settings/RuntimeConfigSettings.tsx"]
    n2["frontend/src/services/systemSettingsService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/systemSettings.md"
    click n1 "../modules/RuntimeConfigSettings.md"
    click n2 "../modules/systemSettingsService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [systemSettings](../modules/systemSettings.md) | 0 | `api_key`, `api_url`, `clear_api_key`, `max_output_tokens`, `model`, `provider`, `reset_fields`, `temperature` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `RuntimeConfigSettings` | import | [RuntimeConfigSettings](../modules/RuntimeConfigSettings.md) | — |
| `systemSettingsService` | import | [systemSettingsService](../modules/systemSettingsService.md) | — |
