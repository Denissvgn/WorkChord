# PlanMasterPage Module

**Path:** `frontend/src/pages/PlanMasterPage.tsx`

## Description

_Auto-generated from `frontend/src/pages/PlanMasterPage.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/common/useConfirmDialog` | `useConfirmDialog` | — | compiler-dependent |
| `../components/feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `../components/feedback/toast` | `useToast` | — | compiler-dependent |
| `../components/layout/Breadcrumbs` | `Breadcrumbs` | — | compiler-dependent |
| `../components/planning/PlanQuickAddCapacity` | `PlanQuickAddCapacity` | — | compiler-dependent |
| `../components/ui/MasterProgress` | `MasterProgress` | — | compiler-dependent |
| `../features/planningMasters/masters` | `PlanReadiness`, `StepStatus` | Declaration | erased |
| `../features/planningMasters/masters` | `derivePlanningRecovery`, `localizeStatus`, `readiness`, `STEP_DEFS`, `nextStep` | — | compiler-dependent |
| `../features/planningMasters/planningReturn` | `PlanningStepId` | Declaration | erased |
| `../features/planningMasters/planningReturn` | `isPlanningStepId`, `PLAN_RETURNED_PARAM`, `withPlanMasterReturn` | — | compiler-dependent |
| `../features/planningMasters/planningTaskIssues` | `PlanningTaskIssue` | Declaration | erased |
| `../features/planningMasters/planningTaskIssues` | `PLANNING_ITERATION_PARAM`, `planningIssueTasksHref` | — | compiler-dependent |
| `../features/planningMasters/usePlanningReadiness` | `PlanningQueryFeedback` | Declaration | erased |
| `../features/planningMasters/usePlanningReadiness` | `usePlanningReadiness` | — | compiler-dependent |
| `../services/planShareService` | `PlanShare` | Declaration | erased |
| `../services/planShareService` | `planShareService` | — | compiler-dependent |
| `../utils/copyText` | `copyText` | — | compiler-dependent |
| `../utils/focusLifecycle` | `captureFocusOrigin`, `focusOwnedTarget` | — | compiler-dependent |
| `../utils/formatDate` | `formatDate`, `formatDateTime` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `lucide-react` | `ArrowRight`, `CalendarRange`, `Check`, `Copy`, `ExternalLink`, `GanttChartSquare`, `ListChecks`, `RefreshCw`, `Share2`, `ShieldAlert`, `Users` | — | compiler-dependent |
| `react` | `ReactNode`, `RefObject` | Declaration | erased |
| `react` | `useCallback`, `useEffect`, `useMemo`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link`, `useSearchParams` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |
| Constants | `STEP_ICONS`, `STEP_STATE_LABEL_KEYS`, `STEP_PRESENTATION_LABEL_KEYS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/pages/PlanMasterPage.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/PlanMasterPage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (1) |
| Outbound | `frontend` (14) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

> All 15 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [RecoveryFocusIntent](../entities/RecoveryFocusIntent.md) | Interface | 77 | — | — |
| [ShareFocusIntent](../entities/ShareFocusIntent.md) | Interface | 84 | — | — |
| [StepDataState](../entities/StepDataState.md) | Type alias | 58 | <pre><code>&#123;&#10;    loading&#58; boolean&#59;&#10;    fetching&#58; boolean&#59;&#10;    error&#58; unknown&#59;&#10;    retry&#58; &#40;&#41; &#61;&#62; Promise&#60;unknown&#62; &#124; unknown&#59;&#10;    label&#58; string&#59;&#10;&#125;</code></pre> | — |
| [EvidenceItem](../entities/EvidenceItem.md) | Type alias | 66 | <pre><code>&#123;&#10;    label&#58; string&#59;&#10;    value&#58; string&#59;&#10;    exception&#63;&#58; boolean&#59;&#10;    href&#63;&#58; string&#59;&#10;    actionLabel&#63;&#58; string&#59;&#10;&#125;</code></pre> | — |
| [RecoveryFocusTarget](../entities/RecoveryFocusTarget.md) | Type alias | 74 | `'iterations' \| 'stale' \| 'step'` | — |
| [ShareFocusTarget](../entities/ShareFocusTarget.md) | Type alias | 75 | `'ready' \| 'retry' \| 'shared'` | — |
| [StepPresentationState](../entities/StepPresentationState.md) | Type alias | 106 | `StepStatus['state'] \| 'loading' \| 'unavailable'` | — |
