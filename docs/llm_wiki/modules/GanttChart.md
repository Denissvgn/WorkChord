# GanttChart Module

**Path:** `frontend/src/components/gantt/GanttChart.tsx`

## Description

_Auto-generated from `frontend/src/components/gantt/GanttChart.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/dateLocale` | `dateFnsLocale` | — | compiler-dependent |
| `../../services/ganttService` | `ganttService` | — | compiler-dependent |
| `../../types/gantt` | `GanttTask`, `SchedulePreviewResponse` | Declaration | erased |
| `../../utils/formatDate` | `formatDate` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/Checkbox` | `Checkbox` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `../feedback/toast` | `useToast` | — | compiler-dependent |
| `../ui` | `OverflowMenu`, `SlideOverDrawer` | — | compiler-dependent |
| `../ui/tone` | `STATUS_TONE`, `toneSolidClassName` | — | compiler-dependent |
| `./TaskEditModal` | `TaskEditModal` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQueryClient` | — | compiler-dependent |
| `@tanstack/react-virtual` | `useVirtualizer` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `date-fns` | `eachDayOfInterval`, `format`, `isSameDay`, `addDays`, `differenceInCalendarDays`, `parseISO`, `startOfDay` | — | compiler-dependent |
| `lucide-react` | `RefreshCw`, `ChevronRight`, `ChevronDown`, `ZoomIn`, `ZoomOut`, `Minimize2`, `Maximize2`, `Calendar`, `CalendarOff`, `ListFilter`, `Eye` | — | compiler-dependent |
| `react` | `useState`, `useMemo`, `useRef`, `useEffect`, `useCallback`, `useId` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `GanttChart` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/gantt/GanttChart.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/GanttChart.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (2) |
| Outbound | `frontend` (11) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 8 | 0 |

> All 13 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [GanttChartProps](../entities/GanttChartProps.md) | Interface | 22 | — | — |
| [FlattenedTask](../entities/GanttChart_FlattenedTask.md) | Interface | 35 | `GanttTask` | — |
| [TaskTimelineDates](../entities/TaskTimelineDates.md) | Interface | 39 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `GanttChart` | <pre><code>&#40;&#123;&#10;    iterationId&#44;&#10;    iterationRevision&#44;    startDate&#44;&#10;    endDate&#44;&#10;    tasks&#44;&#10;    weekends&#44;&#10;    holidays&#44;&#10;    memberVacations&#44;&#10;    sandboxMode &#61; false&#44;&#10;    onSaveSandbox&#44;&#10;&#125;&#58; GanttChartProps&#41;</code></pre> | — | — |
