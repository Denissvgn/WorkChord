# UserSession

**Location:** `frontend/src/services/sessionService.ts:3`
**Kind:** Class
**Bases:** —
**Module:** [sessionService](../modules/sessionService.md)

## Description

_Auto-generated from `UserSession` in `frontend/src/services/sessionService.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `principal_id` | `number \| null` | No | — | — |
| `authenticated` | `boolean` | No | — | — |
| `id` | `number` | Yes | — | — |
| `public_id` | `string` | Yes | — | — |
| `display_name` | `string` | Yes | — | — |
| `created_at` | `string` | Yes | — | — |
| `last_seen_at` | `string` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["UserSession (frontend/src/services/sessionService.ts)"]
    n1["frontend/src/components/UserSessionBadge.tsx"]
    n1 --> n0
    click n0 "../modules/sessionService.md"
    click n1 "../modules/UserSessionBadge.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [sessionService](../modules/sessionService.md) | 0 | `authenticated`, `created_at`, `display_name`, `id`, `last_seen_at`, `principal_id`, `public_id` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `UserSessionBadge` | import | [UserSessionBadge](../modules/UserSessionBadge.md) | — |
