# IterationSelector Module

**Path:** `frontend/src/components/iteration/IterationSelector.tsx`

## Description

_Auto-generated from `frontend/src/components/iteration/IterationSelector.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../../store/iterationStore` | `useIterationStore`, `pickDefaultIteration` | — | compiler-dependent |
| `../../types/iteration` | `Iteration` | Declaration | erased |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `react` | `useEffect` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `IterationSelector` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/feedback/QueryState.tsx"]
    n1["frontend/src/components/iteration/IterationSelector.tsx"]
    n2["frontend/src/pages/GanttPage.tsx"]
    n3["frontend/src/pages/TasksPage.tsx"]
    n4["frontend/src/pages/TeamPage.tsx"]
    n5["frontend/src/services/iterationService.ts"]
    n6["frontend/src/store/iterationStore.ts"]
    n7["frontend/src/types/iteration.ts"]
    n1 --> n0
    n1 --> n5
    n1 --> n6
    n1 --> n7
    n2 --> n1
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n3 --> n0
    n3 --> n1
    n3 --> n5
    n3 --> n6
    n4 --> n0
    n4 --> n1
    n4 --> n5
    n4 --> n6
    n5 --> n7
    click n0 "../modules/QueryState.md"
    click n1 "../modules/IterationSelector.md"
    click n2 "../modules/GanttPage.md"
    click n3 "../modules/TasksPage.md"
    click n4 "../modules/TeamPage.md"
    click n5 "../modules/iterationService.md"
    click n6 "../modules/iterationStore.md"
    click n7 "../modules/types_iteration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GanttPage](../modules/GanttPage.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Inbound | [TeamPage](../modules/TeamPage.md) |
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
| [IterationSelectorProps](../entities/IterationSelectorProps.md) | Interface | 10 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `IterationSelector` | <pre><code>&#40;&#123;&#10;    className&#44;&#10;    onChange&#44;&#10;    showLabel &#61; false&#44;&#10;    disabled &#61; false&#44;&#10;&#125;&#58; IterationSelectorProps&#41;</code></pre> | — | — |
