# AdminAccessPanel.test Module

**Path:** `frontend/src/components/settings/AdminAccessPanel.test.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/AdminAccessPanel.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../test/renderWithProviders` | `createTestQueryClient`, `renderWithProviders` | — | compiler-dependent |
| `./AdminAccessPanel` | `AdminAccessPanel` | — | compiler-dependent |
| `@testing-library/react` | `screen` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `adminAccessHookMock`, `adminAccessStorageMock`, `PROTECTED_QUERY_PREFIXES` |
| Module calls | `adminAccessHookMock = hoisted`, `adminAccessStorageMock = hoisted`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/AdminAccessPanel.test.tsx"]
    n1["frontend/src/components/settings/AdminAccessPanel.tsx"]
    n2["frontend/src/i18n/i18n.ts"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n3 --> n2
    click n0 "../modules/AdminAccessPanel.test.md"
    click n1 "../modules/AdminAccessPanel.md"
    click n2 "../modules/i18n.md"
    click n3 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [AdminAccessPanel](../modules/AdminAccessPanel.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
