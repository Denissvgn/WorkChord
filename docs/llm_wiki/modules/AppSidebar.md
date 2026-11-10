# AppSidebar Module

**Path:** `frontend/src/components/layout/AppSidebar.tsx`

## Description

_Auto-generated from `frontend/src/components/layout/AppSidebar.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/seedDisplay` | `savedViewDisplay` | — | compiler-dependent |
| `../../navigation/workspaces` | `NavItem` | Declaration | erased |
| `../../navigation/workspaces` | `getWorkspaceForPath` | — | compiler-dependent |
| `../../services/savedViewService` | `savedViewService` | — | compiler-dependent |
| `../../types/savedView` | `SavedView` | Declaration | erased |
| `./SidebarIterationCard` | `SidebarIterationCard` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `lucide-react` | `ArrowRight`, `Bookmark`, `ChevronRight`, `ListFilter`, `Search`, `Sparkles`, `TriangleAlert` | — | compiler-dependent |
| `react` | `useEffect`, `useId`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link`, `useLocation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AppSidebar`, `SidebarAttentionAction`, `SidebarContent` |
| Constants | `SYSTEM_VIEW_ORDER`, `SAVED_VIEW_ROUTE_PATHS`, `COMPACT_SAVED_VIEW_LIMIT`, `SAVED_VIEW_SEARCH_LIMIT`, `SAVED_VIEW_TYPES` |
| Module calls | `SAVED_VIEW_ROUTE_PATHS = Set` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/layout/AppShell.tsx"]
    n1["frontend/src/components/layout/AppSidebar.test.tsx"]
    n2["frontend/src/components/layout/AppSidebar.tsx"]
    n3["frontend/src/components/layout/AppTopNav.tsx"]
    n4["frontend/src/components/layout/SidebarIterationCard.tsx"]
    n5["frontend/src/i18n/seedDisplay.ts"]
    n6["frontend/src/navigation/workspaces.ts"]
    n7["frontend/src/services/savedViewService.ts"]
    n8["frontend/src/types/savedView.ts"]
    n0 --> n2
    n0 --> n3
    n1 --> n2
    n1 --> n8
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n2 --> n8
    n3 --> n2
    n3 --> n6
    n5 --> n8
    n7 --> n8
    click n0 "../modules/AppShell.md"
    click n1 "../modules/AppSidebar.test.md"
    click n2 "../modules/AppSidebar.md"
    click n3 "../modules/AppTopNav.md"
    click n4 "../modules/SidebarIterationCard.md"
    click n5 "../modules/seedDisplay.md"
    click n6 "../modules/workspaces.md"
    click n7 "../modules/savedViewService.md"
    click n8 "../modules/savedView.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AppShell](../modules/AppShell.md) |
| Inbound | [AppSidebar.test](../modules/AppSidebar.test.md) |
| Inbound | [AppTopNav](../modules/AppTopNav.md) |
| Outbound | [SidebarIterationCard](../modules/SidebarIterationCard.md) |
| Outbound | [seedDisplay](../modules/seedDisplay.md) |
| Outbound | [workspaces](../modules/workspaces.md) |
| Outbound | [savedViewService](../modules/savedViewService.md) |
| Outbound | [savedView](../modules/savedView.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [SidebarAttentionAction](../entities/SidebarAttentionAction.md) | Interface | 24 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `SidebarContent` | <pre><code>&#40;&#123;&#10;    attentionAction&#44;&#10;    onNavigate&#44;&#10;&#125;&#58; &#123;&#10;    attentionAction&#63;&#58; SidebarAttentionAction&#59;&#10;    onNavigate&#63;&#58; &#40;&#41; &#61;&#62; void&#59;&#10;&#125;&#41;</code></pre> | — | — |
| `AppSidebar` | `()` | — | — |
