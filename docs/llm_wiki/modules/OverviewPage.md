# OverviewPage Module

**Path:** `frontend/src/pages/OverviewPage.tsx`

## Description

_Auto-generated from `frontend/src/pages/OverviewPage.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/common/Button` | `Button` | — | compiler-dependent |
| `../components/feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `../components/tasks/WorkMetricsLine` | `WorkMetricsLine` | — | compiler-dependent |
| `../components/ui` | `InlineEmptyState`, `PageHeader`, `PageLayout`, `SectionCard` | — | compiler-dependent |
| `../components/ui/tone` | `PillTone` | Declaration | erased |
| `../components/ui/tone` | `STATUS_TONE`, `toneVar`, `toneSoftVar` | — | compiler-dependent |
| `../features/overview/attentionRanking` | `AttentionKind`, `AttentionSeverity` | Specifier | compiler-dependent |
| `../features/overview/attentionRanking` | `rankAttentionItems`, `rankAttentionTaskCandidates` | — | compiler-dependent |
| `../features/overview/overviewTaskThread` | `overviewTaskDrawerHref`, `overviewTaskReturnFocusId` | — | compiler-dependent |
| `../features/planningMasters/masters` | `STEP_DEFS` | — | compiler-dependent |
| `../features/planningMasters/planningTaskIssues` | `taskMatchesPlanningIssue` | — | compiler-dependent |
| `../features/planningMasters/usePlanningReadiness` | `PlanningQueryFeedback` | Declaration | erased |
| `../features/planningMasters/usePlanningReadiness` | `usePlanningReadiness` | — | compiler-dependent |
| `../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../services/projectService` | `projectService` | — | compiler-dependent |
| `../types/iteration` | `Iteration` | Declaration | erased |
| `../types/project` | `ProjectSummary`, `ProjectTargetDateRisk`, `ProjectUpdateFreshness` | Declaration | erased |
| `../types/task` | `Task`, `TaskStatus` | Declaration | erased |
| `../utils/apiError` | `getApiErrorStatus` | — | compiler-dependent |
| `../utils/formatDate` | `formatDate` | — | compiler-dependent |
| `../utils/selectWorkNowTasks` | `selectWorkNowTasks` | — | compiler-dependent |
| `../utils/workNumbers` | `formatDecimal`, `formatPercent` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `i18next` | `TFunction` | Declaration | erased |
| `lucide-react` | `LucideIcon` | Declaration | erased |
| `lucide-react` | `Activity`, `AlertTriangle`, `ArrowRight`, `Bookmark`, `Calendar`, `CheckCircle2`, `ChevronDown`, `Clock`, `FolderOpen`, `Inbox`, `ListTodo`, `RefreshCw`, `Target`, `User`, `Zap` | — | compiler-dependent |
| `react` | `ReactNode` | Declaration | erased |
| `react` | `useEffect`, `useMemo`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link`, `useLocation`, `useNavigate` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |
| Constants | `MS_PER_DAY`, `HOURS_PER_DAY`, `CAPACITY_WARNING_PERCENT`, `PACE_WARNING_POINTS`, `ITERATION_DETAILS_ID`, `WORK_NOW_TITLE_ID`, `doneStatuses`, `invalidCachedStatuses`, `operationalAttentionIds`, `commitmentAttentionIds` |
| Module calls | `doneStatuses = Set`, `invalidCachedStatuses = Set`, `operationalAttentionIds = Set`, `commitmentAttentionIds = Set` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/pages/OverviewPage.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/OverviewPage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (1) |
| Outbound | `frontend` (19) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 7 | 0 |

> All 20 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [OverviewFocusPanelProps](../entities/OverviewFocusPanelProps.md) | Interface | 1023 | — | — |
| [OverviewDeliverySnapshotProps](../entities/OverviewDeliverySnapshotProps.md) | Interface | 1110 | — | — |
| [CapacityException](../entities/CapacityException.md) | Type alias | 56 | <pre><code>&#123;&#10;    id&#58; number&#59;&#10;    name&#58; string&#59;&#10;    position&#58; string&#59;&#10;    allocatedDays&#58; number&#59;&#10;    capacityDays&#58; number&#59;&#10;    utilizationPercent&#58; number&#59;&#10;    tone&#58; PillTone&#59;&#10;&#125;</code></pre> | — |
| [AttentionItem](../entities/AttentionItem.md) | Type alias | 66 | <pre><code>&#123;&#10;    id&#58; string&#59;&#10;    kind&#58; AttentionKind&#59;&#10;    severity&#58; AttentionSeverity&#59;&#10;    urgency&#58; number&#59;&#10;    magnitude&#58; number&#59;&#10;    tone&#58; PillTone&#59;&#10;    icon&#58; LucideIcon&#59;&#10;    title&#58; string&#59;&#10;    meta&#58; string&#59;&#10;    to&#58; string&#59;&#10;    actionLabel&#58; string&#59;&#10;&#125;</code></pre> | — |
| [OverviewDataSource](../entities/OverviewDataSource.md) | Type alias | 80 | <pre><code>&#123;&#10;    id&#58; string&#59;&#10;    label&#58; string&#59;&#10;    enabled&#58; boolean&#59;&#10;    hasData&#58; boolean&#59;&#10;    hasUsableData&#58; boolean&#59;&#10;    dataUpdatedAt&#58; number&#59;&#10;    isLoading&#58; boolean&#59;&#10;    isFetching&#58; boolean&#59;&#10;    isError&#58; boolean&#59;&#10;    error&#58; unknown&#59;&#10;    refetch&#58; &#40;&#41; &#61;&#62; Promise&#60;unknown&#62;&#59;&#10;&#125;</code></pre> | — |
| [DirectQueryFeedback](../entities/DirectQueryFeedback.md) | Type alias | 94 | <pre><code>&#123;&#10;    data&#58; unknown&#59;&#10;    dataUpdatedAt&#58; number&#59;&#10;    error&#58; unknown&#59;&#10;    isLoading&#58; boolean&#59;&#10;    isFetching&#58; boolean&#59;&#10;    isError&#58; boolean&#59;&#10;    refetch&#58; &#40;&#41; &#61;&#62; Promise&#60;unknown&#62;&#59;&#10;&#125;</code></pre> | — |
| [OverviewLocationState](../entities/OverviewLocationState.md) | Type alias | 104 | <pre><code>&#123;&#10;    returnFocusId&#63;&#58; string&#59;&#10;&#125;</code></pre> | — |
