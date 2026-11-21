# IterationCapacityLine Module

**Path:** `frontend/src/components/iteration/IterationCapacityLine.tsx`

## Description

_Auto-generated from `frontend/src/components/iteration/IterationCapacityLine.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Button` | `Button` | — | compiler-dependent |
| `../../features/planningMasters/usePlanningNavigationSummary` | `planningNavigationSummaryKey` | — | compiler-dependent |
| `../../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../../utils/workNumbers` | `formatDecimal` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `IterationCapacityLine` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/capacity/TeamList.test.tsx"]
    n1["frontend/src/components/common/Button.tsx"]
    n2["frontend/src/components/iteration/IterationCapacityLine.tsx"]
    n3["frontend/src/components/iteration/IterationList.tsx"]
    n4["frontend/src/features/planningMasters/usePlanningNavigationSummary.ts"]
    n5["frontend/src/services/iterationService.ts"]
    n6["frontend/src/utils/workNumbers.ts"]
    n0 --> n2
    n2 --> n1
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n3 --> n1
    n3 --> n2
    n3 --> n5
    n4 --> n5
    click n0 "../modules/TeamList.test.md"
    click n1 "../modules/Button.md"
    click n2 "../modules/IterationCapacityLine.md"
    click n3 "../modules/IterationList.md"
    click n4 "../modules/usePlanningNavigationSummary.md"
    click n5 "../modules/iterationService.md"
    click n6 "../modules/workNumbers.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TeamList.test](../modules/TeamList.test.md) |
| Inbound | [IterationList](../modules/IterationList.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [usePlanningNavigationSummary](../modules/usePlanningNavigationSummary.md) |
| Outbound | [iterationService](../modules/iterationService.md) |
| Outbound | [workNumbers](../modules/workNumbers.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `IterationCapacityLine` | `({ iterationId }: { iterationId: number })` | — | One labelled capacity bar per iteration: planned hours against capacity, tasks, and whether a schedule exists. |
