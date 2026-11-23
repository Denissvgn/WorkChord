# LegacyRedirect Module

**Path:** `frontend/src/navigation/LegacyRedirect.tsx`

## Description

_Auto-generated from `frontend/src/navigation/LegacyRedirect.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./legacyPaths` | `mapLegacyPath` | — | compiler-dependent |
| `react` | `ReactNode` | Declaration | erased |
| `react-router-dom` | `Navigate`, `useLocation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `LegacyRedirect` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/App.tsx"]
    n1["frontend/src/navigation/CalendarRedirect.test.tsx"]
    n2["frontend/src/navigation/legacyPaths.ts"]
    n3["frontend/src/navigation/LegacyRedirect.test.tsx"]
    n4["frontend/src/navigation/LegacyRedirect.tsx"]
    n5["frontend/src/pages/PlanIterations.test.tsx"]
    n6["frontend/src/pages/PlanPage.test.tsx"]
    n7["frontend/src/pages/ProjectsPage.test.tsx"]
    n8["frontend/src/pages/TasksPage.pipeline.test.tsx"]
    n0 --> n4
    n1 --> n4
    n3 --> n4
    n4 --> n2
    n5 --> n4
    n6 --> n4
    n7 --> n4
    n8 --> n4
    click n0 "../modules/App.md"
    click n1 "../modules/CalendarRedirect.test.md"
    click n2 "../modules/legacyPaths.md"
    click n3 "../modules/LegacyRedirect.test.md"
    click n4 "../modules/LegacyRedirect.md"
    click n5 "../modules/PlanIterations.test.md"
    click n6 "../modules/PlanPage.test.md"
    click n7 "../modules/ProjectsPage.test.md"
    click n8 "../modules/TasksPage.pipeline.test.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [App](../modules/App.md) |
| Inbound | [CalendarRedirect.test](../modules/CalendarRedirect.test.md) |
| Inbound | [LegacyRedirect.test](../modules/LegacyRedirect.test.md) |
| Inbound | [PlanIterations.test](../modules/PlanIterations.test.md) |
| Inbound | [PlanPage.test](../modules/PlanPage.test.md) |
| Inbound | [ProjectsPage.test](../modules/ProjectsPage.test.md) |
| Inbound | [TasksPage.pipeline.test](../modules/TasksPage.pipeline.test.md) |
| Outbound | [legacyPaths](../modules/legacyPaths.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `LegacyRedirect` | `({ children }: { children?: ReactNode })` | — | — |
