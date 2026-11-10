# ProjectsPage.test Module

**Path:** `frontend/src/pages/ProjectsPage.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/ProjectsPage.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `./ProjectsPage` | `ProjectsPage` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `within` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `projectServiceMock`, `savedViewServiceMock`, `project` |
| Module calls | `projectServiceMock = hoisted`, `savedViewServiceMock = hoisted`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/i18n/i18n.ts"]
    n1["frontend/src/pages/ProjectsPage.test.tsx"]
    n2["frontend/src/pages/ProjectsPage.tsx"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n3 --> n0
    click n0 "../modules/i18n.md"
    click n1 "../modules/ProjectsPage.test.md"
    click n2 "../modules/ProjectsPage.md"
    click n3 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [ProjectsPage](../modules/ProjectsPage.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
