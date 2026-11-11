# AdminAccessGate.test Module

**Path:** `frontend/src/components/settings/AdminAccessGate.test.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/AdminAccessGate.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/identity/identityContext` | `IdentityContext` | — | compiler-dependent |
| `../../features/identity/identityService` | `WorkspaceIdentity` | Declaration | erased |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `./AdminAccessGate` | `AdminAccessGate` | — | compiler-dependent |
| `@testing-library/react` | `screen` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/settings/AdminAccessGate.test.tsx"]
    n1["frontend/src/components/settings/AdminAccessGate.tsx"]
    n2["frontend/src/features/identity/identityContext.ts"]
    n3["frontend/src/features/identity/identityService.ts"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n2 --> n3
    click n0 "../modules/AdminAccessGate.test.md"
    click n1 "../modules/AdminAccessGate.md"
    click n2 "../modules/identityContext.md"
    click n3 "../modules/identityService.md"
    click n4 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [AdminAccessGate](../modules/AdminAccessGate.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [identityService](../modules/identityService.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
