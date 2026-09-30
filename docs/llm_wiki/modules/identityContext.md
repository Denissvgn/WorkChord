# identityContext Module

**Path:** `frontend/src/features/identity/identityContext.ts`

## Description

_Auto-generated from `frontend/src/features/identity/identityContext.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./identityService` | `WorkspaceIdentity` |
| `react` | `createContext`, `useContext` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `IdentityContext`, `useIdentity` |
| Constants | `IdentityContext` |
| Module calls | `IdentityContext = createContext` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/TaskForm.tsx"]
    n1["frontend/src/components/UserSessionBadge.tsx"]
    n2["frontend/src/features/identity/identityContext.ts"]
    n3["frontend/src/features/identity/IdentityProvider.tsx"]
    n4["frontend/src/features/identity/identityService.ts"]
    n5["frontend/src/hooks/useAdminAccess.ts"]
    n0 --> n2
    n1 --> n2
    n1 --> n3
    n2 --> n4
    n3 --> n2
    n3 --> n4
    n5 --> n2
    click n0 "../modules/TaskForm.md"
    click n1 "../modules/UserSessionBadge.md"
    click n2 "../modules/identityContext.md"
    click n3 "../modules/IdentityProvider.md"
    click n4 "../modules/identityService.md"
    click n5 "../modules/useAdminAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [UserSessionBadge](../modules/UserSessionBadge.md) |
| Inbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Inbound | [useAdminAccess](../modules/useAdminAccess.md) |
| Outbound | [identityService](../modules/identityService.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [IdentityContextValue](../entities/IdentityContextValue.md) | Type alias | 4 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useIdentity` | `()` | — | — |
