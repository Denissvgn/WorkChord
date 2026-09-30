# PlanPage Module

**Path:** `frontend/src/pages/PlanPage.tsx`

## Description

_Auto-generated from `frontend/src/pages/PlanPage.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../components/feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` |
| `../components/ui` | `PageHeader`, `PageLayout` |
| `../features/planningMasters/masters` | `localizeStatus`, `STEP_DEFS` |
| `../features/planningMasters/usePlanningReadiness` | `usePlanningReadiness` |
| `../utils/formatDate` | `formatDate` |
| `lucide-react` | `ArrowRight`, `CalendarRange`, `Check`, `ChevronDown`, `GanttChartSquare`, `Inbox`, `Layers`, `ListTodo`, `LockKeyhole`, `RefreshCw`, `Sparkles`, `TriangleAlert`, `Users`, `LucideIcon` |
| `react` | `useState` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `Link` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/feedback/QueryState.tsx"]
    n1["frontend/src/components/ui/index.ts"]
    n2["frontend/src/features/planningMasters/masters.ts"]
    n3["frontend/src/features/planningMasters/usePlanningReadiness.ts"]
    n4["frontend/src/pages/PlanPage.test.tsx"]
    n5["frontend/src/pages/PlanPage.tsx"]
    n6["frontend/src/utils/formatDate.ts"]
    n3 --> n2
    n4 --> n2
    n4 --> n5
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n6
    click n0 "../modules/QueryState.md"
    click n1 "../modules/index.md"
    click n2 "../modules/planningMasters_masters.md"
    click n3 "../modules/usePlanningReadiness.md"
    click n4 "../modules/PlanPage.test.md"
    click n5 "../modules/PlanPage.md"
    click n6 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PlanPage.test](../modules/PlanPage.test.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [index](../modules/index.md) |
| Outbound | [planningMasters_masters](../modules/planningMasters_masters.md) |
| Outbound | [usePlanningReadiness](../modules/usePlanningReadiness.md) |
| Outbound | [formatDate](../modules/formatDate.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [LocalizedStepStatus](../entities/LocalizedStepStatus.md) | Type alias | 26 | — | — |
| [PlanningJob](../entities/PlanningJob.md) | Type alias | 32 | — | — |
| [RefreshStatus](../entities/RefreshStatus.md) | Type alias | 41 | — | — |
