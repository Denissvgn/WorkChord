# GitHubRuntimeSettingsUpdate

**Location:** `frontend/src/types/systemSettings.ts:48`
**Kind:** Class
**Bases:** —
**Module:** [systemSettings](../modules/systemSettings.md)

## Description

_Auto-generated from `GitHubRuntimeSettingsUpdate` in `frontend/src/types/systemSettings.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `api_url` | `string` | No | — | — |
| `token` | `string \| null` | No | — | — |
| `clear_token` | `boolean` | No | — | — |
| `request_timeout_seconds` | `number` | No | — | — |
| `webhook_secret` | `string \| null` | No | — | — |
| `clear_webhook_secret` | `boolean` | No | — | — |
| `webhook_create_triage_for_unmatched` | `boolean` | No | — | — |
| `reset_fields` | `string[]` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GitHubRuntimeSettingsUpdate (frontend/src/types/systemSettings.ts)"]
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
| [systemSettings](../modules/systemSettings.md) | 0 | `api_url`, `clear_token`, `clear_webhook_secret`, `request_timeout_seconds`, `reset_fields`, `token`, `webhook_create_triage_for_unmatched`, `webhook_secret` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `RuntimeConfigSettings` | import | [RuntimeConfigSettings](../modules/RuntimeConfigSettings.md) | — |
| `systemSettingsService` | import | [systemSettingsService](../modules/systemSettingsService.md) | — |
