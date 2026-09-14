# routeModules Module

**Path:** `frontend/src/navigation/routeModules.ts`

## Description

_Auto-generated from `frontend/src/navigation/routeModules.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `react-router-dom` | `matchPath` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `RouteModuleKey`, `metadataForPath`, `routeMetadata`, `routeModuleLoaders`, `warmRouteModule` |
| Constants | `routeModuleLoaders`, `routeMetadata` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/App.tsx"]
    n1["frontend/src/components/layout/AppTopNav.tsx"]
    n2["frontend/src/components/layout/DocumentMetadata.tsx"]
    n3["frontend/src/navigation/helpContexts.ts"]
    n4["frontend/src/navigation/routeModules.ts"]
    n0 --> n2
    n0 --> n4
    n1 --> n4
    n2 --> n4
    n3 --> n4
    click n0 "../modules/App.md"
    click n1 "../modules/AppTopNav.md"
    click n2 "../modules/DocumentMetadata.md"
    click n3 "../modules/helpContexts.md"
    click n4 "../modules/routeModules.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [App](../modules/App.md) |
| Inbound | [AppTopNav](../modules/AppTopNav.md) |
| Inbound | [DocumentMetadata](../modules/DocumentMetadata.md) |
| Inbound | [helpContexts](../modules/helpContexts.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [RouteModuleKey](../entities/RouteModuleKey.md) | Type alias | 26 | — | — |
| [RouteMetadata](../entities/RouteMetadata.md) | Type alias | 28 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `metadataForPath` | `(pathname: string) -> RouteMetadata` | — | — |
| `warmRouteModule` | *(async)* `(pathname: string)` | — | — |
