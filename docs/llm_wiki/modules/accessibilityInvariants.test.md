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
| `../navigation/routeModules` | `routeModuleLoaders` | — | compiler-dependent |
| `./accessibilityInvariants` | `accessibleNameViolations`, `headingOrderViolations`, `summaryNameViolations` | — | compiler-dependent |
| `./renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `./routeRegistry` | `routeRegistry` | — | compiler-dependent |
| `./workspaceApi` | `installWorkspaceApi` | — | compiler-dependent |
| `@testing-library/dom` | `getRoles` | — | compiler-dependent |
| `@testing-library/react` | `act`, `waitFor` | — | compiler-dependent |
| `dom-accessibility-api` | `computeAccessibleName` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeAll`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `PAGE`, `TRIAGE_ITEM`, `SHELL_AND_PAGE_READS`, `DIAGNOSTIC_LIMIT`, `BARE_ROUTES` |
| Module calls | `afterEach`, `describe`, `BARE_ROUTES = Set`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/App.tsx"]
    n1["frontend/src/navigation/destinations.ts"]
    n2["frontend/src/navigation/legacyPaths.ts"]
    n3["frontend/src/navigation/routeModules.ts"]
    n4["frontend/src/test/accessibilityInvariants.test.tsx"]
    n5["frontend/src/test/accessibilityInvariants.ts"]
    n6["frontend/src/test/renderWithProviders.tsx"]
    n7["frontend/src/test/routeRegistry.ts"]
    n8["frontend/src/test/workspaceApi.ts"]
    n0 --> n3
    n3 --> n1
    n3 --> n2
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n7 --> n3
    click n0 "../modules/App.md"
    click n1 "../modules/destinations.md"
    click n2 "../modules/legacyPaths.md"
    click n3 "../modules/routeModules.md"
    click n4 "../modules/accessibilityInvariants.test.md"
    click n5 "../modules/accessibilityInvariants.md"
    click n6 "../modules/renderWithProviders.md"
    click n7 "../modules/routeRegistry.md"
    click n8 "../modules/workspaceApi.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [App](../modules/App.md) |
| Outbound | [destinations](../modules/destinations.md) |
| Outbound | [legacyPaths](../modules/legacyPaths.md) |
| Outbound | [routeModules](../modules/routeModules.md) |
| Outbound | [accessibilityInvariants](../modules/accessibilityInvariants.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [routeRegistry](../modules/routeRegistry.md) |
| Outbound | [workspaceApi](../modules/workspaceApi.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |
