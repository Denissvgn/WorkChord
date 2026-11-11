# TasksPage Module

**Path:** `frontend/src/pages/TasksPage.tsx`

## Description

_Auto-generated from `frontend/src/pages/TasksPage.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/common/Button` | `Button` | — | compiler-dependent |
| `../components/common/FullscreenWorkspace` | `FullscreenWorkspace` | — | compiler-dependent |
| `../components/feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `../components/iteration/IterationSelector` | `IterationSelector` | — | compiler-dependent |
| `../components/overview/OverviewTaskReturnBar` | `OverviewTaskReturnBar` | — | compiler-dependent |
| `../components/planning/PlanReturnBar` | `PlanReturnBar` | — | compiler-dependent |
| `../components/tasks/BacklogPanel` | `BacklogPanel` | — | compiler-dependent |
| `../components/tasks/GuardedTaskModal` | `GuardedTaskModal` | — | compiler-dependent |
| `../components/tasks/ImportTasksModal` | `ImportTasksModal` | — | compiler-dependent |
| `../components/tasks/KanbanBoard/KanbanBoard` | `KanbanBoard` | — | compiler-dependent |
| `../components/tasks/QuickCapture` | `QuickCapture` | — | compiler-dependent |
| `../components/tasks/SavedViewsControl` | `SavedViewsControl` | — | compiler-dependent |
| `../components/tasks/TaskEditorDrawer` | `TaskEditorDrawer` | — | compiler-dependent |
| `../components/tasks/TaskFiltersBar` | `TaskFilters` | Declaration | erased |
| `../components/tasks/TaskFiltersBar` | `TaskFiltersBar` | — | compiler-dependent |
| `../components/tasks/TaskList` | `SortKey`, `TaskMode` | Declaration | erased |
| `../components/tasks/TaskList` | `TaskList` | — | compiler-dependent |
| `../components/tasks/TaskReadView` | `TASK_PART_PARAM` | — | compiler-dependent |
| `../components/tasks/TaskSearch` | `TaskSearch` | — | compiler-dependent |
| `../components/ui` | `OverflowMenu`, `PageHeader`, `PageLayout`, `SlideOverDrawer` | — | compiler-dependent |
| `../features/overview/overviewTaskThread` | `OVERVIEW_TASK_ORIGIN`, `OVERVIEW_TASK_ORIGIN_PARAM`, `OVERVIEW_TASK_PARAM`, `OVERVIEW_TASK_RETURN_PARAM`, `OVERVIEW_TASK_THREAD_PARAM`, `overviewTaskThreadSource`, `positiveTaskId` | — | compiler-dependent |
| `../features/planningMasters/planningTaskIssues` | `PlanningTaskIssue` | Declaration | erased |
| `../features/planningMasters/planningTaskIssues` | `PLANNING_ITERATION_PARAM`, `PLANNING_TASK_ISSUE_PARAM`, `parsePlanningIterationId`, `parsePlanningTaskIssue` | — | compiler-dependent |
| `../features/savedViews/taskViewState` | `filtersFromSavedView`, `sortKeyFromSavedView` | — | compiler-dependent |
| `../i18n/seedDisplay` | `savedViewDisplay` | — | compiler-dependent |
| `../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../services/savedViewService` | `savedViewService` | — | compiler-dependent |
| `../services/taskService` | `taskService` | — | compiler-dependent |
| `../store/iterationStore` | `useIterationStore`, `pickDefaultIteration` | — | compiler-dependent |
| `../types/savedView` | `SavedView` | Declaration | erased |
| `../types/task` | `Task` | Declaration | erased |
| `../utils/savedViewState` | `savedViewModified` | — | compiler-dependent |
| `../utils/taskFilterDefaults` | `defaultFilters` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `framer-motion` | `motion` | — | compiler-dependent |
| `lucide-react` | `AlertTriangle`, `Bookmark`, `LayoutGrid`, `List`, `ListFilter`, `Maximize2`, `Minimize2`, `Plus`, `Upload`, `Waypoints`, `X` | — | compiler-dependent |
| `react` | `useCallback`, `useEffect`, `useMemo`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link`, `useSearchParams` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |
| Constants | `PLANNING_ISSUE_COPY_KEYS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/pages/TasksPage.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/TasksPage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (1) |
| Outbound | `frontend` (30) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 7 | 0 |

> All 31 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ViewMode](../entities/ViewMode.md) | Type alias | 69 | `'list' \| 'board'` | — |
