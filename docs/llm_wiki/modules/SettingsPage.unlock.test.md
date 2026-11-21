# SettingsPage.unlock.test Module

**Path:** `frontend/src/pages/SettingsPage.unlock.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/SettingsPage.unlock.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../features/identity/identityContext` | `IdentityContext` | — | compiler-dependent |
| `../features/identity/identityService` | `WorkspaceIdentity` | Declaration | erased |
| `../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../utils/adminAccess` | `ADMIN_API_KEY_STORAGE_KEY` | — | compiler-dependent |
| `./SettingsPage` | `SettingsPage` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `within` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |
| Unresolved `dynamic-import` | — (line 18; deferred) | — | unclassified |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `verifyKey`, `{ field, selfLockingField }`, `PROTECTED` |
| Module calls | `verifyKey = hoisted`, `mock`, `{ field, selfLockingField } = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/features/identity/identityContext.ts"]
    n1["frontend/src/features/identity/identityService.ts"]
    n2["frontend/src/pages/SettingsPage.tsx"]
    n3["frontend/src/pages/SettingsPage.unlock.test.tsx"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n5["frontend/src/utils/adminAccess.ts"]
    n0 --> n1
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    n3 --> n5
    click n0 "../modules/identityContext.md"
    click n1 "../modules/identityService.md"
    click n2 "../modules/SettingsPage.md"
    click n3 "../modules/SettingsPage.unlock.test.md"
    click n4 "../modules/renderWithProviders.md"
    click n5 "../modules/adminAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [identityService](../modules/identityService.md) |
| Outbound | [SettingsPage](../modules/SettingsPage.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [adminAccess](../modules/adminAccess.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
