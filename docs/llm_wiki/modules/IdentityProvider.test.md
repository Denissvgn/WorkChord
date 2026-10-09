# IdentityProvider.test Module

**Path:** `frontend/src/features/identity/IdentityProvider.test.tsx`

## Description

_Auto-generated from `frontend/src/features/identity/IdentityProvider.test.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../test/renderWithProviders` | `renderWithProviders` |
| `../planningMasters/usePlanningNavigationSummary` | `planningNavigationSummaryKey` |
| `./IdentityProvider` | `IdentityProvider`, `IdentityBadge` |
| `@tanstack/react-query` | `useQueryClient`, `QueryClient` |
| `@testing-library/react` | `screen`, `waitFor`, `act` |
| `react` | `useEffect` |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `service` |
| Module calls | `service = hoisted`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/identity/IdentityProvider.test.tsx"]
    n1["frontend/src/features/identity/IdentityProvider.tsx"]
    n2["frontend/src/features/planningMasters/usePlanningNavigationSummary.ts"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    click n0 "../modules/IdentityProvider.test.md"
    click n1 "../modules/IdentityProvider.md"
    click n2 "../modules/usePlanningNavigationSummary.md"
    click n3 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Outbound | [usePlanningNavigationSummary](../modules/usePlanningNavigationSummary.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |
