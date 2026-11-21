# AdminAccessPanel.test Module

**Path:** `frontend/src/components/settings/AdminAccessPanel.test.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/AdminAccessPanel.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/identity/IdentityProvider` | `IdentityProvider` | — | compiler-dependent |
| `../../features/identity/identityContext` | `IdentityContext` | — | compiler-dependent |
| `../../features/identity/identityService` | `WorkspaceIdentity` | Declaration | erased |
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../services/api` | `api`, `IDENTITY_EXPIRED_EVENT`, `setSessionIntegrity` | — | compiler-dependent |
| `../../test/renderWithProviders` | `createTestQueryClient`, `renderWithProviders` | — | compiler-dependent |
| `../../utils/adminAccess` | `ADMIN_API_KEY_CHANGED_EVENT`, `getAdminApiKey`, `setAdminApiKey` | — | compiler-dependent |
| `./AdminAccessPanel` | `AdminAccessPanel` | — | compiler-dependent |
| `./protectedQueryKeys` | `protectedQueryKeys` | — | compiler-dependent |
| `@testing-library/react` | `act`, `screen`, `waitFor` | — | compiler-dependent |
| `axios` | `AxiosResponse`, `InternalAxiosRequestConfig` | Declaration | erased |
| `axios` | `AxiosError` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `local`, `originalAdapter`, `server` |
| Module calls | `server = fn`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/settings/AdminAccessPanel.test.tsx"]
    n1["frontend/src/components/settings/AdminAccessPanel.tsx"]
    n2["frontend/src/components/settings/protectedQueryKeys.ts"]
    n3["frontend/src/features/identity/identityContext.ts"]
    n4["frontend/src/features/identity/IdentityProvider.tsx"]
    n5["frontend/src/features/identity/identityService.ts"]
    n6["frontend/src/i18n/i18n.ts"]
    n7["frontend/src/services/api.ts"]
    n8["frontend/src/test/renderWithProviders.tsx"]
    n9["frontend/src/utils/adminAccess.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n0 --> n5
    n0 --> n6
    n0 --> n7
    n0 --> n8
    n0 --> n9
    n1 --> n2
    n1 --> n3
    n1 --> n9
    n3 --> n5
    n4 --> n3
    n4 --> n5
    n4 --> n7
    n4 --> n9
    n5 --> n7
    n7 --> n9
    n8 --> n6
    click n0 "../modules/AdminAccessPanel.test.md"
    click n1 "../modules/AdminAccessPanel.md"
    click n2 "../modules/protectedQueryKeys.md"
    click n3 "../modules/identityContext.md"
    click n4 "../modules/IdentityProvider.md"
    click n5 "../modules/identityService.md"
    click n6 "../modules/i18n.md"
    click n7 "../modules/api.md"
    click n8 "../modules/renderWithProviders.md"
    click n9 "../modules/adminAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [AdminAccessPanel](../modules/AdminAccessPanel.md) |
| Outbound | [protectedQueryKeys](../modules/protectedQueryKeys.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Outbound | [identityService](../modules/identityService.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [adminAccess](../modules/adminAccess.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
