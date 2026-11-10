# SidebarIterationCard Module

**Path:** `frontend/src/components/layout/SidebarIterationCard.tsx`

## Description

_Auto-generated from `frontend/src/components/layout/SidebarIterationCard.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/planningMasters/usePlanningNavigationSummary` | `usePlanningNavigationSummary` | — | compiler-dependent |
| `react` | `KeyboardEvent` | Specifier | compiler-dependent |
| `react` | `useEffect`, `useId`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `SidebarIterationCard` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/layout/AppSidebar.tsx"]
    n1["frontend/src/components/layout/SidebarIterationCard.test.tsx"]
    n2["frontend/src/components/layout/SidebarIterationCard.tsx"]
    n3["frontend/src/features/planningMasters/usePlanningNavigationSummary.ts"]
    n0 --> n2
    n1 --> n2
    n2 --> n3
    click n0 "../modules/AppSidebar.md"
    click n1 "../modules/SidebarIterationCard.test.md"
    click n2 "../modules/SidebarIterationCard.md"
    click n3 "../modules/usePlanningNavigationSummary.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AppSidebar](../modules/AppSidebar.md) |
| Inbound | [SidebarIterationCard.test](../modules/SidebarIterationCard.test.md) |
| Outbound | [usePlanningNavigationSummary](../modules/usePlanningNavigationSummary.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `SidebarIterationCard` | `({ onNavigate }: { onNavigate?: () => void })` | — | — |
