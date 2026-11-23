# AppSidebar Module

**Path:** `frontend/src/components/layout/AppSidebar.tsx`

## Description

_Auto-generated from `frontend/src/components/layout/AppSidebar.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/planningMasters/usePlanningNavigationSummary` | `usePlanningNavigationSummary` | — | compiler-dependent |
| `../../features/scope/useScopeLink` | `useScopeLink` | — | compiler-dependent |
| `../../navigation/destinations` | `Destination`, `DestinationCounterValues` | Declaration | erased |
| `../../navigation/destinations` | `DESTINATION_GROUPS`, `formatDestinationCounter`, `getCounterSource`, `getDestinationForPath` | — | compiler-dependent |
| `../../services/triageService` | `triageService` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react` | `useId` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link`, `useLocation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AppSidebar`, `SidebarContent` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/layout/AppShell.tsx"]
    n1["frontend/src/components/layout/AppSidebar.planProgress.test.tsx"]
    n2["frontend/src/components/layout/AppSidebar.test.tsx"]
    n3["frontend/src/components/layout/AppSidebar.tsx"]
    n4["frontend/src/components/layout/AppTopNav.test.tsx"]
    n5["frontend/src/components/layout/AppTopNav.tsx"]
    n6["frontend/src/components/layout/planProgressPlacement.test.tsx"]
    n7["frontend/src/components/layout/shellViewport.test.tsx"]
    n8["frontend/src/features/planningMasters/usePlanningNavigationSummary.ts"]
    n9["frontend/src/features/scope/useScopeLink.ts"]
    n10["frontend/src/navigation/destinations.ts"]
    n11["frontend/src/services/triageService.ts"]
    n0 --> n3
    n0 --> n5
    n1 --> n3
    n2 --> n3
    n3 --> n8
    n3 --> n9
    n3 --> n10
    n3 --> n11
    n4 --> n3
    n4 --> n5
    n5 --> n3
    n5 --> n9
    n5 --> n10
    n6 --> n3
    n7 --> n3
    n7 --> n5
    click n0 "../modules/AppShell.md"
    click n1 "../modules/AppSidebar.planProgress.test.md"
    click n2 "../modules/AppSidebar.test.md"
    click n3 "../modules/AppSidebar.md"
    click n4 "../modules/AppTopNav.test.md"
    click n5 "../modules/AppTopNav.md"
    click n6 "../modules/planProgressPlacement.test.md"
    click n7 "../modules/shellViewport.test.md"
    click n8 "../modules/usePlanningNavigationSummary.md"
    click n9 "../modules/useScopeLink.md"
    click n10 "../modules/destinations.md"
    click n11 "../modules/triageService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AppShell](../modules/AppShell.md) |
| Inbound | [AppSidebar.planProgress.test](../modules/AppSidebar.planProgress.test.md) |
| Inbound | [AppSidebar.test](../modules/AppSidebar.test.md) |
| Inbound | [AppTopNav.test](../modules/AppTopNav.test.md) |
| Inbound | [AppTopNav](../modules/AppTopNav.md) |
| Inbound | [planProgressPlacement.test](../modules/planProgressPlacement.test.md) |
| Inbound | [shellViewport.test](../modules/shellViewport.test.md) |
| Outbound | [usePlanningNavigationSummary](../modules/usePlanningNavigationSummary.md) |
| Outbound | [useScopeLink](../modules/useScopeLink.md) |
| Outbound | [destinations](../modules/destinations.md) |
| Outbound | [triageService](../modules/triageService.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `SidebarContent` | `({ onNavigate }: { onNavigate?: () => void })` | — | The ten destinations in their groups. The desktop sidebar and the drawer both render this. |
| `AppSidebar` | `()` | — | — |
