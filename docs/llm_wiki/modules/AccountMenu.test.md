# AccountMenu.test Module

**Path:** `frontend/src/features/identity/AccountMenu.test.tsx`

## Description

_Auto-generated from `frontend/src/features/identity/AccountMenu.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/layout/AppTopNav` | `AppTopNav` | — | compiler-dependent |
| `../../services/api` | `api`, `IDENTITY_EXPIRED_EVENT` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../utils/adminAccess` | `clearAdminApiKey`, `hasAdminApiKey` | — | compiler-dependent |
| `./AccountMenu` | `IdentityBadge` | — | compiler-dependent |
| `./IdentityProvider` | `IdentityProvider` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor`, `within` | — | compiler-dependent |
| `axios` | `AxiosAdapter`, `AxiosResponse`, `InternalAxiosRequestConfig` | Declaration | erased |
| `axios` | `AxiosError` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `originalAdapter`, `service`, `team`, `topBarMocks`, `localWorkspace` |
| Module calls | `service = hoisted`, `mock`, `team = hoisted`, `mock`, `topBarMocks = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/layout/AppTopNav.tsx"]
    n1["frontend/src/features/identity/AccountMenu.test.tsx"]
    n2["frontend/src/features/identity/AccountMenu.tsx"]
    n3["frontend/src/features/identity/IdentityProvider.tsx"]
    n4["frontend/src/services/api.ts"]
    n5["frontend/src/test/renderWithProviders.tsx"]
    n6["frontend/src/utils/adminAccess.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n2 --> n4
    n2 --> n6
    n3 --> n4
    n3 --> n6
    n4 --> n6
    click n0 "../modules/AppTopNav.md"
    click n1 "../modules/AccountMenu.test.md"
    click n2 "../modules/AccountMenu.md"
    click n3 "../modules/IdentityProvider.md"
    click n4 "../modules/api.md"
    click n5 "../modules/renderWithProviders.md"
    click n6 "../modules/adminAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [AppTopNav](../modules/AppTopNav.md) |
| Outbound | [AccountMenu](../modules/AccountMenu.md) |
| Outbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [adminAccess](../modules/adminAccess.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
