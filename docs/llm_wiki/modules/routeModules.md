# routeModules Module

**Path:** `frontend/src/navigation/routeModules.ts`

## Description

_Auto-generated from `frontend/src/navigation/routeModules.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./destinations` | `DestinationId` | Specifier | compiler-dependent |
| `./destinations` | `getDestination` | — | compiler-dependent |
| `./legacyPaths` | `mapLegacyPath` | — | compiler-dependent |
| `react-router-dom` | `matchPath` | — | compiler-dependent |
| Unresolved `dynamic-import` | — (line 6; deferred) | — | unclassified |
| Unresolved `dynamic-import` | — (line 7; deferred) | — | unclassified |
| Unresolved `dynamic-import` | — (line 8; deferred) | — | unclassified |
| Unresolved `dynamic-import` | — (line 9; deferred) | — | unclassified |
| Unresolved `dynamic-import` | — (line 10; deferred) | — | unclassified |
| Unresolved `dynamic-import` | — (line 11; deferred) | — | unclassified |
| Unresolved `dynamic-import` | — (line 12; deferred) | — | unclassified |
| Unresolved `dynamic-import` | — (line 13; deferred) | — | unclassified |
| Unresolved `dynamic-import` | — (line 14; deferred) | — | unclassified |
| Unresolved `dynamic-import` | — (line 15; deferred) | — | unclassified |
| Unresolved `dynamic-import` | — (line 16; deferred) | — | unclassified |
| Unresolved `dynamic-import` | — (line 17; deferred) | — | unclassified |
| Unresolved `dynamic-import` | — (line 18; deferred) | — | unclassified |
| Unresolved `dynamic-import` | — (line 19; deferred) | — | unclassified |
| Unresolved `dynamic-import` | — (line 20; deferred) | — | unclassified |
| Unresolved `dynamic-import` | — (line 21; deferred) | — | unclassified |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `RouteModuleKey`, `metadataForPath`, `routeMetadata`, `routeModuleLoaders`, `warmRouteModule` |
| Constants | `routeModuleLoaders`, `routeMetadata` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/App.tsx"]
    n1["frontend/src/components/layout/AppTopNav.tsx"]
    n2["frontend/src/components/layout/DocumentMetadata.tsx"]
    n3["frontend/src/navigation/destinations.test.ts"]
    n4["frontend/src/navigation/destinations.ts"]
    n5["frontend/src/navigation/helpContexts.ts"]
    n6["frontend/src/navigation/legacyPaths.ts"]
    n7["frontend/src/navigation/routeModules.ts"]
    n8["frontend/src/test/pageChrome.test.tsx"]
    n9["frontend/src/test/routeRegistry.ts"]
    n10["frontend/src/test/scopedPageRender.test.tsx"]
    n0 --> n2
    n0 --> n7
    n1 --> n4
    n1 --> n7
    n2 --> n7
    n3 --> n4
    n3 --> n7
    n5 --> n4
    n5 --> n7
    n7 --> n4
    n7 --> n6
    n8 --> n4
    n8 --> n7
    n8 --> n9
    n9 --> n7
    n10 --> n7
    click n0 "../modules/App.md"
    click n1 "../modules/AppTopNav.md"
    click n2 "../modules/DocumentMetadata.md"
    click n3 "../modules/destinations.test.md"
    click n4 "../modules/destinations.md"
    click n5 "../modules/helpContexts.md"
    click n6 "../modules/legacyPaths.md"
    click n7 "../modules/routeModules.md"
    click n8 "../modules/pageChrome.test.md"
    click n9 "../modules/routeRegistry.md"
    click n10 "../modules/scopedPageRender.test.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [App](../modules/App.md) |
| Inbound | [AppTopNav](../modules/AppTopNav.md) |
| Inbound | [DocumentMetadata](../modules/DocumentMetadata.md) |
| Inbound | [destinations.test](../modules/destinations.test.md) |
| Inbound | [helpContexts](../modules/helpContexts.md) |
| Inbound | [pageChrome.test](../modules/pageChrome.test.md) |
| Inbound | [routeRegistry](../modules/routeRegistry.md) |
| Inbound | [scopedPageRender.test](../modules/scopedPageRender.test.md) |
| Outbound | [destinations](../modules/destinations.md) |
| Outbound | [legacyPaths](../modules/legacyPaths.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [RouteModuleKey](../entities/RouteModuleKey.md) | Type alias | 24 | `keyof typeof routeModuleLoaders` | — |
| [RouteMetadata](../entities/RouteMetadata.md) | Type alias | 26 | <pre><code>&#123;&#10;    key&#58; RouteModuleKey&#59;&#10;    path&#58; string&#59;&#10;    titleKey&#58; string&#59;&#10;&#125;</code></pre> | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `metadataForPath` | `(pathname: string) -> RouteMetadata` | — | — |
| `warmRouteModule` | *(async)* `(pathname: string)` | — | — |
