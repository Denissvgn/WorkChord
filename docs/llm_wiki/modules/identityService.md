# identityService Module

**Path:** `frontend/src/features/identity/identityService.ts`

## Description

_Auto-generated from `frontend/src/features/identity/identityService.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/api` | `api` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `WorkProfile`, `WorkspaceIdentity`, `identityService` |
| Constants | `identityService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/settings/AdminAccessGate.test.tsx"]
    n1["frontend/src/features/identity/identityContext.ts"]
    n2["frontend/src/features/identity/IdentityProvider.tsx"]
    n3["frontend/src/features/identity/identityService.ts"]
    n4["frontend/src/features/identity/LocalProfilePicker.tsx"]
    n5["frontend/src/services/api.ts"]
    n0 --> n1
    n0 --> n3
    n1 --> n3
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n3 --> n5
    n4 --> n3
    click n0 "../modules/AdminAccessGate.test.md"
    click n1 "../modules/identityContext.md"
    click n2 "../modules/IdentityProvider.md"
    click n3 "../modules/identityService.md"
    click n4 "../modules/LocalProfilePicker.md"
    click n5 "../modules/api.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AdminAccessGate.test](../modules/AdminAccessGate.test.md) |
| Inbound | [identityContext](../modules/identityContext.md) |
| Inbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Inbound | [LocalProfilePicker](../modules/LocalProfilePicker.md) |
| Outbound | [api](../modules/api.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [WorkProfile](../entities/WorkProfile.md) | Interface | 4 | — | A linked profile is verified; a trusted-local session's own choice is not. |
| [WorkspaceIdentity](../entities/WorkspaceIdentity.md) | Interface | 6 | — | — |
