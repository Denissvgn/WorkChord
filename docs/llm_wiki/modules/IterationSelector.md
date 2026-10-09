# IterationSelector Module

**Path:** `frontend/src/components/iteration/IterationSelector.tsx`

## Description

_Auto-generated from `frontend/src/components/iteration/IterationSelector.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/iterationService` | `iterationService` |
| `../../store/iterationStore` | `useIterationStore` |
| `../../types/iteration` | `Iteration` |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` |
| `@tanstack/react-query` | `useQuery` |
| `clsx` | `clsx` |
| `react` | `useEffect` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `IterationSelector` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/feedback/QueryState.tsx"]
    n1["frontend/src/components/iteration/IterationSelector.tsx"]
    n2["frontend/src/pages/GanttPage.tsx"]
    n3["frontend/src/pages/TasksPage.tsx"]
    n4["frontend/src/services/iterationService.ts"]
    n5["frontend/src/store/iterationStore.ts"]
    n6["frontend/src/types/iteration.ts"]
    n1 --> n0
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n2 --> n1
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n3 --> n0
    n3 --> n1
    n3 --> n4
    n3 --> n5
    n4 --> n6
    click n0 "../modules/QueryState.md"
    click n1 "../modules/IterationSelector.md"
    click n2 "../modules/GanttPage.md"
    click n3 "../modules/TasksPage.md"
    click n4 "../modules/iterationService.md"
    click n5 "../modules/iterationStore.md"
    click n6 "../modules/types_iteration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GanttPage](../modules/GanttPage.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [iterationService](../modules/iterationService.md) |
| Outbound | [iterationStore](../modules/iterationStore.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [IterationSelectorProps](../entities/IterationSelectorProps.md) | Class | 10 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `IterationSelector` | `({     className,     onChange,     showLabel = false, }: IterationSelectorProps)` | — | — |
