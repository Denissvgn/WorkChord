# EmailSettingsUpdate

**Location:** `frontend/src/types/emailSettings.ts:16`
**Kind:** Class
**Bases:** —
**Module:** [emailSettings](../modules/emailSettings.md)

## Description

_Auto-generated from `EmailSettingsUpdate` in `frontend/src/types/emailSettings.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `enabled` | `boolean` | Yes | — | — |
| `smtp_host` | `string` | Yes | — | — |
| `smtp_port` | `number` | Yes | — | — |
| `smtp_user` | `string` | Yes | — | — |
| `smtp_password` | `string \| null` | No | — | — |
| `smtp_from_email` | `string` | Yes | — | — |
| `smtp_use_tls` | `boolean` | Yes | — | — |
| `clear_smtp_password` | `boolean` | No | — | — |
| `reset_fields` | `string[]` | No | — | — |

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
