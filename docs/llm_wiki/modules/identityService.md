# identityService Module

**Path:** `frontend/src/features/identity/identityService.ts`

## Description

_Auto-generated from `frontend/src/features/identity/identityService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `WorkspaceIdentity`, `identityService` |
| Constants | `identityService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/identity/identityContext.ts"]
    n1["frontend/src/features/identity/IdentityProvider.tsx"]
    n2["frontend/src/features/identity/identityService.ts"]
    n3["frontend/src/services/api.ts"]
    n0 --> n2
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n2 --> n3
    click n0 "../modules/identityContext.md"
    click n1 "../modules/IdentityProvider.md"
    click n2 "../modules/identityService.md"
    click n3 "../modules/api.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [identityContext](../modules/identityContext.md) |
| Inbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Outbound | [api](../modules/api.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [WorkspaceIdentity](../entities/WorkspaceIdentity.md) | Class | 3 | — | — |
