# routeRegistry Module

**Path:** `frontend/src/test/routeRegistry.ts`

## Description

_Auto-generated from `frontend/src/test/routeRegistry.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../navigation/routeModules` | `RouteModuleKey` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `routeRegistry` |
| Constants | `routeRegistry` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/navigation/routeModules.ts"]
    n1["frontend/src/test/accessibilityInvariants.test.tsx"]
    n2["frontend/src/test/pageChrome.test.tsx"]
    n3["frontend/src/test/routeRegistry.ts"]
    n1 --> n0
    n1 --> n3
    n2 --> n0
    n2 --> n3
    n3 --> n0
    click n0 "../modules/routeModules.md"
    click n1 "../modules/accessibilityInvariants.test.md"
    click n2 "../modules/pageChrome.test.md"
    click n3 "../modules/routeRegistry.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [accessibilityInvariants.test](../modules/accessibilityInvariants.test.md) |
| Inbound | [pageChrome.test](../modules/pageChrome.test.md) |
| Outbound | [routeModules](../modules/routeModules.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [RouteStatus](../entities/RouteStatus.md) | Type alias | 3 | `{ key: RouteModuleKey; status: 'migrated' \| 'pending'; path: string }` | — |
