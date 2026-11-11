# WorkProfile

**Location:** `frontend/src/features/identity/identityService.ts:4`
**Kind:** Interface
**Bases:** —
**Module:** [identityService](../modules/identityService.md)

## Description

A linked profile is verified; a trusted-local session's own choice is not.

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `display_name` | `string` | Yes | — | — |
| `verified` | `boolean` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WorkProfile (frontend/src/features/identity/identityService.ts)"]
    n1["LocalProfilePicker (frontend/src/features/identity/LocalProfilePicker.tsx)"]
    n1 --> n0
    click n0 "../modules/identityService.md"
    click n1 "../modules/LocalProfilePicker.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [identityService](../modules/identityService.md) | 0 | `display_name`, `id`, `verified` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `LocalProfilePicker` | type_reference | [LocalProfilePicker](../modules/LocalProfilePicker.md) | — |
