# AppTopNav Module

**Path:** `frontend/src/components/layout/AppTopNav.tsx`

## Description

_Auto-generated from `frontend/src/components/layout/AppTopNav.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../features/planningMasters/usePlanningNavigationSummary` | `usePlanningNavigationSummary` |
| `../../navigation/routeModules` | `warmRouteModule` |
| `../../navigation/workspaces` | `getWorkspaceForPath`, `WORKSPACES`, `WorkspaceMetadata` |
| `../../services/triageService` | `triageService` |
| `../UserSessionBadge` | `UserSessionBadge` |
| `../common/dialogLayer` | `useDialogLayer` |
| `./AppSidebar` | `SidebarContent`, `SidebarAttentionAction` |
| `./ContextHelp` | `ContextHelp` |
| `./commandMenuEvents` | `openCommandMenu` |
| `@tanstack/react-query` | `useQuery` |
| `lucide-react` | `AlertTriangle`, `Command`, `Menu`, `X` |
| `react` | `useEffect`, `useRef`, `useState` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `Link`, `useLocation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AppTopNav` |
| Constants | `MOBILE_NAV_TITLE_ID` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/dialogLayer.ts"]
    n1["frontend/src/components/layout/AppShell.tsx"]
    n2["frontend/src/components/layout/AppSidebar.tsx"]
    n3["frontend/src/components/layout/AppTopNav.test.tsx"]
    n4["frontend/src/components/layout/AppTopNav.tsx"]
    n5["frontend/src/components/layout/commandMenuEvents.ts"]
    n6["frontend/src/components/layout/ContextHelp.tsx"]
    n7["frontend/src/components/UserSessionBadge.tsx"]
    n8["frontend/src/features/planningMasters/usePlanningNavigationSummary.ts"]
    n9["frontend/src/navigation/routeModules.ts"]
    n10["frontend/src/navigation/workspaces.ts"]
    n11["frontend/src/services/triageService.ts"]
    n1 --> n2
    n1 --> n4
    n2 --> n10
    n3 --> n4
    n4 --> n0
    n4 --> n2
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n4 --> n9
    n4 --> n10
    n4 --> n11
    n6 --> n5
    click n0 "../modules/dialogLayer.md"
    click n1 "../modules/AppShell.md"
    click n2 "../modules/AppSidebar.md"
    click n3 "../modules/AppTopNav.test.md"
    click n4 "../modules/AppTopNav.md"
    click n5 "../modules/commandMenuEvents.md"
    click n6 "../modules/ContextHelp.md"
    click n7 "../modules/UserSessionBadge.md"
    click n8 "../modules/usePlanningNavigationSummary.md"
    click n9 "../modules/routeModules.md"
    click n10 "../modules/workspaces.md"
    click n11 "../modules/triageService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AppShell](../modules/AppShell.md) |
| Inbound | [AppTopNav.test](../modules/AppTopNav.test.md) |
| Outbound | [dialogLayer](../modules/dialogLayer.md) |
| Outbound | [AppSidebar](../modules/AppSidebar.md) |
| Outbound | [commandMenuEvents](../modules/commandMenuEvents.md) |
| Outbound | [ContextHelp](../modules/ContextHelp.md) |
| Outbound | [UserSessionBadge](../modules/UserSessionBadge.md) |
| Outbound | [usePlanningNavigationSummary](../modules/usePlanningNavigationSummary.md) |
| Outbound | [routeModules](../modules/routeModules.md) |
| Outbound | [workspaces](../modules/workspaces.md) |
| Outbound | [triageService](../modules/triageService.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [WorkspaceAttention](../entities/WorkspaceAttention.md) | Class | 18 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `AppTopNav` | `()` | — | — |
