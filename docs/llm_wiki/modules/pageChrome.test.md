# pageChrome.test Module

**Path:** `frontend/src/test/pageChrome.test.tsx`

## Description

_Auto-generated from `frontend/src/test/pageChrome.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/common/Button` | `Button` | — | compiler-dependent |
| `../components/common/Select` | `Select` | — | compiler-dependent |
| `../components/ui` | `FilterBar`, `PageHeader`, `PageToolbar`, `ViewSwitch` | — | compiler-dependent |
| `../navigation/destinations` | `DESTINATIONS` | — | compiler-dependent |
| `../navigation/routeModules` | `routeMetadata`, `routeModuleLoaders` | — | compiler-dependent |
| `./pageChrome` | `expectPageChrome` | — | compiler-dependent |
| `./renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `./routeRegistry` | `routeRegistry` | — | compiler-dependent |
| `./workspaceApi` | `installWorkspaceApi` | — | compiler-dependent |
| `@testing-library/react` | `act`, `waitFor` | — | compiler-dependent |
| `react-router-dom` | `Route`, `Routes` | — | compiler-dependent |
| `vitest` | `afterEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `afterEach`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Select.tsx"]
    n2["frontend/src/components/ui/index.ts"]
    n3["frontend/src/navigation/destinations.ts"]
    n4["frontend/src/navigation/routeModules.ts"]
    n5["frontend/src/test/pageChrome.test.tsx"]
    n6["frontend/src/test/pageChrome.ts"]
    n7["frontend/src/test/renderWithProviders.tsx"]
    n8["frontend/src/test/routeRegistry.ts"]
    n9["frontend/src/test/workspaceApi.ts"]
    n4 --> n3
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n4
    n5 --> n6
    n5 --> n7
    n5 --> n8
    n5 --> n9
    n8 --> n4
    click n0 "../modules/Button.md"
    click n1 "../modules/Select.md"
    click n2 "../modules/index.md"
    click n3 "../modules/destinations.md"
    click n4 "../modules/routeModules.md"
    click n5 "../modules/pageChrome.test.md"
    click n6 "../modules/pageChrome.md"
    click n7 "../modules/renderWithProviders.md"
    click n8 "../modules/routeRegistry.md"
    click n9 "../modules/workspaceApi.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Select](../modules/Select.md) |
| Outbound | [index](../modules/index.md) |
| Outbound | [destinations](../modules/destinations.md) |
| Outbound | [routeModules](../modules/routeModules.md) |
| Outbound | [pageChrome](../modules/pageChrome.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [routeRegistry](../modules/routeRegistry.md) |
| Outbound | [workspaceApi](../modules/workspaceApi.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
