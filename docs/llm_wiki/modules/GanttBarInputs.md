# GanttBarInputs Module

**Path:** `frontend/src/components/gantt/GanttBarInputs.tsx`

## Description

_Auto-generated from `frontend/src/components/gantt/GanttBarInputs.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/teamService` | `teamService` | — | compiler-dependent |
| `../../types/gantt` | `GanttTask` | Declaration | erased |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react` | `useEffect`, `useId`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `GanttBarInputChanges`, `GanttBarInputs` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/components/gantt/GanttBarInputs.tsx"]
    n3["frontend/src/components/gantt/GanttChart.tsx"]
    n4["frontend/src/services/teamService.ts"]
    n5["frontend/src/types/gantt.ts"]
    n1 --> n0
    n2 --> n0
    n2 --> n1
    n2 --> n4
    n2 --> n5
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n5
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/GanttBarInputs.md"
    click n3 "../modules/GanttChart.md"
    click n4 "../modules/teamService.md"
    click n5 "../modules/types_gantt.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GanttChart](../modules/GanttChart.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [types_gantt](../modules/types_gantt.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [GanttBarInputChanges](../entities/GanttBarInputChanges.md) | Interface | 9 | — | — |
| [GanttBarInputsProps](../entities/GanttBarInputsProps.md) | Interface | 17 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `GanttBarInputs` | `({ task, iterationId, taskOptions, anchor, onApply, onMoreFields, onClose }: GanttBarInputsProps)` | — | The five inputs that move a task's dates. Dates themselves are scheduler |
