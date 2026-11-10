# AppSidebar.test Module

**Path:** `frontend/src/components/layout/AppSidebar.test.tsx`

## Description

_Auto-generated from `frontend/src/components/layout/AppSidebar.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/savedView` | `SavedView` | Declaration | erased |
| `./AppSidebar` | `AppSidebar`, `SidebarContent` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor`, `within` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `savedViewServiceMock`, `systemTaskView` |
| Module calls | `savedViewServiceMock = hoisted`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/layout/AppSidebar.test.tsx"]
    n1["frontend/src/components/layout/AppSidebar.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n3["frontend/src/types/savedView.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n3
    click n0 "../modules/AppSidebar.test.md"
    click n1 "../modules/AppSidebar.md"
    click n2 "../modules/renderWithProviders.md"
    click n3 "../modules/savedView.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [AppSidebar](../modules/AppSidebar.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [savedView](../modules/savedView.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
