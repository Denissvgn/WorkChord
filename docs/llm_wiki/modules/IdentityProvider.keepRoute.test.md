# IdentityProvider.keepRoute.test Module

**Path:** `frontend/src/features/identity/IdentityProvider.keepRoute.test.tsx`

## Description

_Auto-generated from `frontend/src/features/identity/IdentityProvider.keepRoute.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../pages/TeamPage` | `TeamPage` | — | compiler-dependent |
| `../../services/api` | `api`, `setSessionIntegrity` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../utils/adminAccess` | `clearAdminApiKey`, `getAdminApiKey` | — | compiler-dependent |
| `../firstRun/FirstRunLanding` | `FirstRunLanding` | — | compiler-dependent |
| `./IdentityProvider` | `IdentityProvider` | — | compiler-dependent |
| `@testing-library/react` | `act`, `screen`, `waitFor` | — | compiler-dependent |
| `axios` | `AxiosResponse`, `InternalAxiosRequestConfig` | Declaration | erased |
| `axios` | `AxiosError` | — | compiler-dependent |
| `react-router-dom` | `Link`, `Route`, `Routes`, `useLocation` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `local`, `originalAdapter` |
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/firstRun/FirstRunLanding.tsx"]
    n1["frontend/src/features/identity/IdentityProvider.keepRoute.test.tsx"]
    n2["frontend/src/features/identity/IdentityProvider.tsx"]
    n3["frontend/src/pages/TeamPage.tsx"]
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
    n4 --> n6
    click n0 "../modules/FirstRunLanding.md"
    click n1 "../modules/IdentityProvider.keepRoute.test.md"
    click n2 "../modules/IdentityProvider.md"
    click n3 "../modules/TeamPage.md"
    click n4 "../modules/api.md"
    click n5 "../modules/renderWithProviders.md"
    click n6 "../modules/adminAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [FirstRunLanding](../modules/FirstRunLanding.md) |
| Outbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Outbound | [TeamPage](../modules/TeamPage.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [adminAccess](../modules/adminAccess.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |
