# EmailSettingsUpdate

**Location:** `frontend/src/types/emailSettings.ts:16`
**Kind:** Class
**Bases:** —
**Module:** [emailSettings](../modules/emailSettings.md)

## Description

_Auto-generated from `EmailSettingsUpdate` in `frontend/src/types/emailSettings.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `enabled` | `boolean` | *required* | — |
| `smtp_host` | `string` | *required* | — |
| `smtp_port` | `number` | *required* | — |
| `smtp_user` | `string` | *required* | — |
| `smtp_password` | `string \| null` | *required* | — |
| `smtp_from_email` | `string` | *required* | — |
| `smtp_use_tls` | `boolean` | *required* | — |
| `clear_smtp_password` | `boolean` | *required* | — |
| `reset_fields` | `string[]` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["EmailSettingsUpdate (frontend/src/types/emailSettings.ts)"]
    n1["frontend/src/services/emailSettingsService.ts"]
    n1 --> n0
    click n0 "../modules/emailSettings.md"
    click n1 "../modules/emailSettingsService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [emailSettings](../modules/emailSettings.md) | 0 | `clear_smtp_password`, `enabled`, `reset_fields`, `smtp_from_email`, `smtp_host`, `smtp_password`, `smtp_port`, `smtp_use_tls`, `smtp_user` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `emailSettingsService` | import | [emailSettingsService](../modules/emailSettingsService.md) | — |
