# GitHubRuntimeSettingsUpdate

**Location:** `frontend/src/types/systemSettings.ts:48`
**Kind:** Class
**Bases:** —
**Module:** [systemSettings](../modules/systemSettings.md)

## Description

_Auto-generated from `GitHubRuntimeSettingsUpdate` in `frontend/src/types/systemSettings.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `api_url` | `string` | *required* | — |
| `token` | `string \| null` | *required* | — |
| `clear_token` | `boolean` | *required* | — |
| `request_timeout_seconds` | `number` | *required* | — |
| `webhook_secret` | `string \| null` | *required* | — |
| `clear_webhook_secret` | `boolean` | *required* | — |
| `webhook_create_triage_for_unmatched` | `boolean` | *required* | — |
| `reset_fields` | `string[]` | *required* | — |

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
