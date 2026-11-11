# WorkspaceIdentity

**Location:** `frontend/src/features/identity/identityService.ts:6`
**Kind:** Interface
**Bases:** —
**Module:** [identityService](../modules/identityService.md)

## Description

_Auto-generated from `WorkspaceIdentity` in `frontend/src/features/identity/identityService.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `mode` | `'managed' \| 'trusted_local'` | Yes | — | — |
| `authenticated` | `boolean` | Yes | — | — |
| `configured` | `boolean` | Yes | — | — |
| `principal` | `{ id: number; kind: 'human' \| 'agent' \| 'system'; display_name: string } \| null` | Yes | — | — |
| `profile` | `WorkProfile \| null` | Yes | — | — |
| `workspace_role` | `'owner' \| 'operator' \| 'member' \| null` | Yes | — | — |
| `projects` | `Record<string, string>` | Yes | — | — |
| `csrf_token` | `string \| null` | Yes | — | — |
| `authentication_error` | `string \| null` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WorkspaceIdentity (frontend/src/features/identity/identityService.ts)"]
    n1["frontend/src/components/settings/AdminAccessGate.test.tsx"]
    n2["frontend/src/features/identity/identityContext.ts"]
    n3["frontend/src/features/identity/IdentityProvider.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/identityService.md"
    click n1 "../modules/AdminAccessGate.test.md"
    click n2 "../modules/identityContext.md"
    click n3 "../modules/IdentityProvider.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [identityService](../modules/identityService.md) | 0 | `authenticated`, `authentication_error`, `configured`, `csrf_token`, `mode`, `principal`, `profile`, `projects`, `workspace_role` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AdminAccessGate.test` | import | [AdminAccessGate.test](../modules/AdminAccessGate.test.md) | — |
| `identityContext` | import | [identityContext](../modules/identityContext.md) | — |
| `IdentityProvider` | import | [IdentityProvider](../modules/IdentityProvider.md) | — |
