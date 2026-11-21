# accessibilityInvariants.test Module

**Path:** `frontend/src/test/accessibilityInvariants.test.tsx`

## Description

_Auto-generated from `frontend/src/test/accessibilityInvariants.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../App` | `App` | — | compiler-dependent |
| `../navigation/destinations` | `getDestinationForPath` | — | compiler-dependent |
| `../navigation/legacyPaths` | `mapLegacyPath` | — | compiler-dependent |
| `./accessibilityInvariants` | `accessibleNameViolations`, `headingOrderViolations`, `summaryNameViolations` | — | compiler-dependent |
| `./renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `./routeRegistry` | `routeRegistry` | — | compiler-dependent |
| `./workspaceApi` | `installWorkspaceApi` | — | compiler-dependent |
| `@testing-library/dom` | `getRoles` | — | compiler-dependent |
| `@testing-library/react` | `act`, `waitFor` | — | compiler-dependent |
| `dom-accessibility-api` | `computeAccessibleName` | — | compiler-dependent |
| `vitest` | `afterEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `PAGE`, `TRIAGE_ITEM`, `SHELL_AND_PAGE_READS`, `BARE_ROUTES` |
| Module calls | `afterEach`, `describe`, `BARE_ROUTES = Set`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/App.tsx"]
    n1["frontend/src/navigation/destinations.ts"]
    n2["frontend/src/navigation/legacyPaths.ts"]
    n3["frontend/src/test/accessibilityInvariants.test.tsx"]
    n4["frontend/src/test/accessibilityInvariants.ts"]
    n5["frontend/src/test/renderWithProviders.tsx"]
    n6["frontend/src/test/routeRegistry.ts"]
    n7["frontend/src/test/workspaceApi.ts"]
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n3 --> n7
    click n0 "../modules/App.md"
    click n1 "../modules/destinations.md"
    click n2 "../modules/legacyPaths.md"
    click n3 "../modules/accessibilityInvariants.test.md"
    click n4 "../modules/accessibilityInvariants.md"
    click n5 "../modules/renderWithProviders.md"
    click n6 "../modules/routeRegistry.md"
    click n7 "../modules/workspaceApi.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [App](../modules/App.md) |
| Outbound | [destinations](../modules/destinations.md) |
| Outbound | [legacyPaths](../modules/legacyPaths.md) |
| Outbound | [accessibilityInvariants](../modules/accessibilityInvariants.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [routeRegistry](../modules/routeRegistry.md) |
| Outbound | [workspaceApi](../modules/workspaceApi.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |
