# AppShell Module

**Path:** `frontend/src/components/layout/AppShell.tsx`

## Description

_Auto-generated from `frontend/src/components/layout/AppShell.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../store/themeStore` | `useThemeStore` |
| `../feedback/WorkRefreshStatus` | `WorkRefreshStatus` |
| `./AppSidebar` | `AppSidebar` |
| `./AppTopNav` | `AppTopNav` |
| `./CommandMenu` | `CommandMenu` |
| `./DocumentMetadata` | `DocumentMetadata` |
| `./RouteErrorBoundary` | `RouteErrorBoundary` |
| `framer-motion` | `MotionConfig` |
| `react` | `ReactNode`, `useEffect`, `useRef` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `useLocation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AppShell` |
| Constants | `SCROLL_LOCK_PATHS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/App.tsx"]
    n1["frontend/src/components/feedback/WorkRefreshStatus.tsx"]
    n2["frontend/src/components/layout/AppShell.test.tsx"]
    n3["frontend/src/components/layout/AppShell.tsx"]
    n4["frontend/src/components/layout/AppSidebar.tsx"]
    n5["frontend/src/components/layout/AppTopNav.tsx"]
    n6["frontend/src/components/layout/CommandMenu.tsx"]
    n7["frontend/src/components/layout/DocumentMetadata.tsx"]
    n8["frontend/src/components/layout/RouteErrorBoundary.tsx"]
    n9["frontend/src/store/themeStore.ts"]
    n0 --> n3
    n0 --> n7
    n2 --> n3
    n3 --> n1
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n3 --> n9
    n5 --> n4
    click n0 "../modules/App.md"
    click n1 "../modules/WorkRefreshStatus.md"
    click n2 "../modules/AppShell.test.md"
    click n3 "../modules/AppShell.md"
    click n4 "../modules/AppSidebar.md"
    click n5 "../modules/AppTopNav.md"
    click n6 "../modules/CommandMenu.md"
    click n7 "../modules/DocumentMetadata.md"
    click n8 "../modules/RouteErrorBoundary.md"
    click n9 "../modules/themeStore.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [App](../modules/App.md) |
| Inbound | [AppShell.test](../modules/AppShell.test.md) |
| Outbound | [WorkRefreshStatus](../modules/WorkRefreshStatus.md) |
| Outbound | [AppSidebar](../modules/AppSidebar.md) |
| Outbound | [AppTopNav](../modules/AppTopNav.md) |
| Outbound | [CommandMenu](../modules/CommandMenu.md) |
| Outbound | [DocumentMetadata](../modules/DocumentMetadata.md) |
| Outbound | [RouteErrorBoundary](../modules/RouteErrorBoundary.md) |
| Outbound | [themeStore](../modules/themeStore.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `AppShell` | `({ children }: { children: ReactNode })` | — | — |
