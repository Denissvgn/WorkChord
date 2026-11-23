# FilterBar.test Module

**Path:** `frontend/src/components/ui/FilterBar.test.tsx`

## Description

_Auto-generated from `frontend/src/components/ui/FilterBar.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `./FilterBar` | `FilterBarFilter` | Specifier | compiler-dependent |
| `./FilterBar` | `FilterBar` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `within` | — | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `tasks`, `definitions` |
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/ui/FilterBar.test.tsx"]
    n1["frontend/src/components/ui/FilterBar.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n0 --> n1
    n0 --> n2
    click n0 "../modules/FilterBar.test.md"
    click n1 "../modules/FilterBar.md"
    click n2 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [FilterBar](../modules/FilterBar.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
