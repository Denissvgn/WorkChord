# AccountSession

**Location:** `frontend/src/features/identity/identityService.ts:24`
**Kind:** Interface
**Bases:** —
**Module:** [identityService](../modules/identityService.md)

## Description

One session of this account, or on a trusted-local server, one paired reader.

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `public_id` | `string` | Yes | — | — |
| `created_at` | `string` | Yes | — | — |
| `expires_at` | `string \| null` | Yes | — | — |
| `revoked_at` | `string \| null` | Yes | — | — |
| `user_agent` | `string \| null` | Yes | — | — |
| `current` | `boolean` | Yes | — | — |
| `access` | `'full' \| 'observe'` | Yes | — | — |
| `client_label` | `string \| null` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AccountSession (frontend/src/features/identity/identityService.ts)"]
    n1["frontend/src/components/settings/ConnectedReadersPanel.tsx"]
    n1 --> n0
    click n0 "../modules/identityService.md"
    click n1 "../modules/ConnectedReadersPanel.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [identityService](../modules/identityService.md) | 0 | `access`, `client_label`, `created_at`, `current`, `expires_at`, `public_id`, `revoked_at`, `user_agent` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `ConnectedReadersPanel` | import | [ConnectedReadersPanel](../modules/ConnectedReadersPanel.md) | — |
