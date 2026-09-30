# AppShell Module

**Path:** `frontend/src/components/layout/AppShell.tsx`

## Description

_Auto-generated from `frontend/src/components/layout/AppShell.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../store/themeStore` | `useThemeStore` |
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
    n1["frontend/src/components/layout/AppShell.test.tsx"]
    n2["frontend/src/components/layout/AppShell.tsx"]
    n3["frontend/src/components/layout/AppSidebar.tsx"]
    n4["frontend/src/components/layout/AppTopNav.tsx"]
    n5["frontend/src/components/layout/CommandMenu.tsx"]
    n6["frontend/src/components/layout/DocumentMetadata.tsx"]
    n7["frontend/src/components/layout/RouteErrorBoundary.tsx"]
    n8["frontend/src/store/themeStore.ts"]
    n0 --> n2
    n0 --> n6
    n1 --> n2
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n2 --> n8
    n4 --> n3
    click n0 "../modules/App.md"
    click n1 "../modules/AppShell.test.md"
    click n2 "../modules/AppShell.md"
    click n3 "../modules/AppSidebar.md"
    click n4 "../modules/AppTopNav.md"
    click n5 "../modules/CommandMenu.md"
    click n6 "../modules/DocumentMetadata.md"
    click n7 "../modules/RouteErrorBoundary.md"
    click n8 "../modules/themeStore.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [App](../modules/App.md) |
| Inbound | [AppShell.test](../modules/AppShell.test.md) |
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
