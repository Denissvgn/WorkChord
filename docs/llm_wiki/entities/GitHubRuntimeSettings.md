# GitHubRuntimeSettings

**Location:** `frontend/src/types/systemSettings.ts:39`
**Kind:** Class
**Bases:** —
**Module:** [systemSettings](../modules/systemSettings.md)

## Description

_Auto-generated from `GitHubRuntimeSettings` in `frontend/src/types/systemSettings.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `api_url` | `string` | *required* | — |
| `request_timeout_seconds` | `number` | *required* | — |
| `webhook_create_triage_for_unmatched` | `boolean` | *required* | — |
| `has_token` | `boolean` | *required* | — |
| `has_webhook_secret` | `boolean` | *required* | — |
| `field_sources` | `Record<string, RuntimeSettingSource>` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GitHubRuntimeSettings (frontend/src/types/systemSettings.ts)"]
    n1["frontend/src/services/systemSettingsService.ts"]
    n1 --> n0
    click n0 "../modules/systemSettings.md"
    click n1 "../modules/systemSettingsService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [systemSettings](../modules/systemSettings.md) | 0 | `api_url`, `field_sources`, `has_token`, `has_webhook_secret`, `request_timeout_seconds`, `webhook_create_triage_for_unmatched` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `systemSettingsService` | import | [systemSettingsService](../modules/systemSettingsService.md) | — |
