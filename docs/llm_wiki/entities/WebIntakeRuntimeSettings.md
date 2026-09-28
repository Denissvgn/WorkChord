# WebIntakeRuntimeSettings

**Location:** `frontend/src/types/systemSettings.ts:59`
**Kind:** Class
**Bases:** —
**Module:** [systemSettings](../modules/systemSettings.md)

## Description

_Auto-generated from `WebIntakeRuntimeSettings` in `frontend/src/types/systemSettings.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `rate_limit_per_minute` | `number` | Yes | — | — |
| `has_token` | `boolean` | Yes | — | — |
| `field_sources` | `Record<string, RuntimeSettingSource>` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WebIntakeRuntimeSettings (frontend/src/types/systemSettings.ts)"]
    n1["frontend/src/services/systemSettingsService.ts"]
    n1 --> n0
    click n0 "../modules/systemSettings.md"
    click n1 "../modules/systemSettingsService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [systemSettings](../modules/systemSettings.md) | 0 | `field_sources`, `has_token`, `rate_limit_per_minute` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `systemSettingsService` | import | [systemSettingsService](../modules/systemSettingsService.md) | — |
