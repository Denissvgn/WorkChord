# NativeConnectionPage.test Module

**Path:** `frontend/src/pages/NativeConnectionPage.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/NativeConnectionPage.test.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../features/identity/identityContext` | `IdentityContext` |
| `../test/renderWithProviders` | `renderWithProviders` |
| `./NativeConnectionPage` | `NativeConnectionPage` |
| `@testing-library/react` | `screen`, `waitFor` |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `service`, `request` |
| Module calls | `service = hoisted`, `mock`, `request = repeat`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/identity/identityContext.ts"]
    n1["frontend/src/pages/NativeConnectionPage.test.tsx"]
    n2["frontend/src/pages/NativeConnectionPage.tsx"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n2 --> n0
    click n0 "../modules/identityContext.md"
    click n1 "../modules/NativeConnectionPage.test.md"
    click n2 "../modules/NativeConnectionPage.md"
    click n3 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [NativeConnectionPage](../modules/NativeConnectionPage.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
