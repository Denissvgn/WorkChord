# UserSessionBadge Module

**Path:** `frontend/src/components/UserSessionBadge.tsx`

## Description

_Auto-generated from `frontend/src/components/UserSessionBadge.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../features/identity/IdentityProvider` | `IdentityBadge` | — | compiler-dependent |
| `../features/identity/identityContext` | `useIdentity` | — | compiler-dependent |
| `../services/sessionService` | `UserSession` | Specifier | compiler-dependent |
| `../services/sessionService` | `sessionService` | — | compiler-dependent |
| `lucide-react` | `User`, `Loader2` | — | compiler-dependent |
| `react` | `useEffect`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `UserSessionBadge` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/layout/AppTopNav.tsx"]
    n1["frontend/src/components/UserSessionBadge.test.tsx"]
    n2["frontend/src/components/UserSessionBadge.tsx"]
    n3["frontend/src/features/identity/identityContext.ts"]
    n4["frontend/src/features/identity/IdentityProvider.tsx"]
    n5["frontend/src/services/sessionService.ts"]
    n0 --> n2
    n1 --> n2
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n4 --> n3
    click n0 "../modules/AppTopNav.md"
    click n1 "../modules/UserSessionBadge.test.md"
    click n2 "../modules/UserSessionBadge.md"
    click n3 "../modules/identityContext.md"
    click n4 "../modules/IdentityProvider.md"
    click n5 "../modules/sessionService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AppTopNav](../modules/AppTopNav.md) |
| Inbound | [UserSessionBadge.test](../modules/UserSessionBadge.test.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Outbound | [sessionService](../modules/sessionService.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `UserSessionBadge` | `()` | — | — |
