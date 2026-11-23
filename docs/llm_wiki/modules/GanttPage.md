# GanttPage Module

**Path:** `frontend/src/pages/GanttPage.tsx`

## Description

Snapshot restore captures the target iteration identity and its observed revision before confirmation. Managed workspace operators use identity-based admin access; conflicts retain the snapshot for explicit comparison without fetching versions at save.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/common/Button` | `Button` | — | compiler-dependent |
| `../components/common/ConfirmDialog` | `ConfirmDialog` | — | compiler-dependent |
| `../components/common/FullscreenWorkspace` | `FullscreenWorkspace` | — | compiler-dependent |
| `../components/common/Modal` | `Modal` | — | compiler-dependent |
| `../components/feedback/toast` | `useToast` | — | compiler-dependent |
| `../components/gantt/GanttChart` | `GanttChart` | — | compiler-dependent |
| `../components/gantt/ScheduleExplanationDetails` | `ScheduleExplanationDetails` | — | compiler-dependent |
| `../components/gantt/TaskEditDrawer` | `TaskEditDrawer` | — | compiler-dependent |
| `../components/planning/PlanningWorkbenchFrame` | `PlanningWorkbenchFrame` | — | compiler-dependent |
| `../components/ui` | `OverflowMenu` | — | compiler-dependent |
| `../components/ui/OverflowMenu` | `OverflowMenuItem` | Declaration | erased |
| `../features/firstRun/NextStepEmptyState` | `NextStepEmptyState` | — | compiler-dependent |
| `../features/firstRun/firstRunSteps` | `firstRunPlanHref` | — | compiler-dependent |
| `../features/scope/useScopeLink` | `useScopeLink` | — | compiler-dependent |
| `../features/scope/useWorkScope` | `useWorkScope` | — | compiler-dependent |
| `../hooks/useAdminAccess` | `useAdminAccess` | — | compiler-dependent |
| `../services/ganttService` | `ganttService` | — | compiler-dependent |
| `../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../services/planningInputService` | `planningInputService` | — | compiler-dependent |
| `../services/snapshotService` | `IterationSnapshot` | Declaration | erased |
| `../services/snapshotService` | `snapshotService` | — | compiler-dependent |
| `../services/taskService` | `taskService` | — | compiler-dependent |
| `../types/gantt` | `ExplainScheduleResponse`, `GanttTask` | Declaration | erased |
| `../types/iteration` | `Iteration` | Declaration | erased |
| `../types/task` | `TaskBatchUpdateItem`, `TaskUpdate` | Declaration | erased |
| `../utils/adminAccess` | `getAdminAccessErrorMessage` | — | compiler-dependent |
| `../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../utils/formatDate` | `formatDateTime` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery`, `useMutation`, `useQueryClient` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `AlertTriangle`, `Sparkles`, `Maximize2`, `Minimize2`, `FlaskConical`, `Undo2`, `Check`, `History`, `RefreshCw` | — | compiler-dependent |
| `react` | `useState`, `useMemo`, `useCallback`, `useRef`, `useId` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |
| Constants | `DECISION_COUNT_LABELS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/pages/GanttPage.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/GanttPage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (4) |
| Outbound | `frontend` (27) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 6 | 0 |

> All 31 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.
