# usePlanningNavigationSummary Module

**Path:** `frontend/src/features/planningMasters/usePlanningNavigationSummary.ts`

## Description

_Auto-generated from `frontend/src/features/planningMasters/usePlanningNavigationSummary.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/iterationService` | `iterationService` |
| `../../store/iterationStore` | `useIterationStore` |
| `../../types/iteration` | `Iteration` |
| `./masters` | `deriveStatus`, `readiness`, `PlanReadiness` |
| `@tanstack/react-query` | `useQuery` |
| `react` | `useMemo` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `planningNavigationSummaryKey`, `usePlanningNavigationSummary` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/layout/AppTopNav.tsx"]
    n1["frontend/src/components/layout/SidebarIterationCard.tsx"]
    n2["frontend/src/features/planningMasters/masters.ts"]
    n3["frontend/src/features/planningMasters/planningNavigationInvalidation.test.ts"]
    n4["frontend/src/features/planningMasters/planningNavigationInvalidation.ts"]
    n5["frontend/src/features/planningMasters/usePlanningNavigationSummary.ts"]
    n6["frontend/src/services/iterationService.ts"]
    n7["frontend/src/store/iterationStore.ts"]
    n8["frontend/src/types/iteration.ts"]
    n0 --> n5
    n1 --> n5
    n3 --> n4
    n3 --> n5
    n4 --> n5
    n5 --> n2
    n5 --> n6
    n5 --> n7
    n5 --> n8
    n6 --> n8
    click n0 "../modules/AppTopNav.md"
    click n1 "../modules/SidebarIterationCard.md"
    click n2 "../modules/planningMasters_masters.md"
    click n3 "../modules/planningNavigationInvalidation.test.md"
    click n4 "../modules/planningNavigationInvalidation.md"
    click n5 "../modules/usePlanningNavigationSummary.md"
    click n6 "../modules/iterationService.md"
    click n7 "../modules/iterationStore.md"
    click n8 "../modules/types_iteration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AppTopNav](../modules/AppTopNav.md) |
| Inbound | [SidebarIterationCard](../modules/SidebarIterationCard.md) |
| Inbound | [planningNavigationInvalidation.test](../modules/planningNavigationInvalidation.test.md) |
| Inbound | [planningNavigationInvalidation](../modules/planningNavigationInvalidation.md) |
| Outbound | [planningMasters_masters](../modules/planningMasters_masters.md) |
| Outbound | [iterationService](../modules/iterationService.md) |
| Outbound | [iterationStore](../modules/iterationStore.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `planningNavigationSummaryKey` | `(iterationId: number)` | — | — |
| `usePlanningNavigationSummary` | `()` | — | — |
