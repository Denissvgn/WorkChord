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
    n0["frontend/src/components/tasks/TaskDiscussion.test.tsx"]
    n1["frontend/src/components/tasks/TaskDiscussion.tsx"]
    n2["frontend/src/components/tasks/TaskForm.tsx"]
    n3["frontend/src/components/UserSessionBadge.tsx"]
    n4["frontend/src/features/identity/identityContext.ts"]
    n5["frontend/src/features/identity/IdentityProvider.tsx"]
    n6["frontend/src/features/identity/identityService.ts"]
    n7["frontend/src/hooks/useAdminAccess.ts"]
    n8["frontend/src/pages/MyWorkPage.tsx"]
    n9["frontend/src/pages/NativeConnectionPage.test.tsx"]
    n10["frontend/src/pages/NativeConnectionPage.tsx"]
    n0 --> n1
    n0 --> n4
    n1 --> n4
    n2 --> n1
    n2 --> n4
    n3 --> n4
    n3 --> n5
    n4 --> n6
    n5 --> n4
    n5 --> n6
    n7 --> n4
    n8 --> n4
    n9 --> n4
    n9 --> n10
    n10 --> n4
    click n0 "../modules/TaskDiscussion.test.md"
    click n1 "../modules/TaskDiscussion.md"
    click n2 "../modules/TaskForm.md"
    click n3 "../modules/UserSessionBadge.md"
    click n4 "../modules/identityContext.md"
    click n5 "../modules/IdentityProvider.md"
    click n6 "../modules/identityService.md"
    click n7 "../modules/useAdminAccess.md"
    click n8 "../modules/MyWorkPage.md"
    click n9 "../modules/NativeConnectionPage.test.md"
    click n10 "../modules/NativeConnectionPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskDiscussion.test](../modules/TaskDiscussion.test.md) |
| Inbound | [TaskDiscussion](../modules/TaskDiscussion.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [UserSessionBadge](../modules/UserSessionBadge.md) |
| Inbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Inbound | [useAdminAccess](../modules/useAdminAccess.md) |
| Inbound | [MyWorkPage](../modules/MyWorkPage.md) |
| Inbound | [NativeConnectionPage.test](../modules/NativeConnectionPage.test.md) |
| Inbound | [NativeConnectionPage](../modules/NativeConnectionPage.md) |
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
