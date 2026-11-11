# ProjectDetailPage Module

**Path:** `frontend/src/pages/ProjectDetailPage.tsx`

## Description

_Auto-generated from `frontend/src/pages/ProjectDetailPage.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/common/Button` | `Button` | — | compiler-dependent |
| `../components/common/ConfirmDialog` | `ConfirmDialog` | — | compiler-dependent |
| `../components/common/Input` | `RequiredIndicator` | — | compiler-dependent |
| `../components/common/Modal` | `Modal` | — | compiler-dependent |
| `../components/feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `../components/feedback/toast` | `useToast` | — | compiler-dependent |
| `../components/layout/Breadcrumbs` | `Breadcrumbs` | — | compiler-dependent |
| `../components/projects/ProjectForm` | `ProjectForm` | — | compiler-dependent |
| `../components/projects/ProjectIterationsSection` | `ProjectIterationsSection` | — | compiler-dependent |
| `../components/projects/ProjectTaskTree` | `ProjectTaskTree` | — | compiler-dependent |
| `../components/projects/TimeEntriesReport` | `TimeEntriesReport` | — | compiler-dependent |
| `../components/projects/projectStatusStyles` | `projectStatusBadgeClassName`, `projectStatusPillClassName` | — | compiler-dependent |
| `../components/releases/ReleaseForm` | `ReleaseForm` | — | compiler-dependent |
| `../components/requestSources/RequestSourceLinksPanel` | `RequestSourceLinksPanel` | — | compiler-dependent |
| `../components/tasks/GuardedTaskModal` | `GuardedTaskModal` | — | compiler-dependent |
| `../components/ui` | `InlineEmptyState`, `OverflowMenu`, `PageHeader`, `PageLayout`, `Pill`, `SectionCard`, `SlideOverDrawer`, `StatusSegmentStrip`, `StickyRail` | — | compiler-dependent |
| `../components/ui/tone` | `STATUS_TONE` | — | compiler-dependent |
| `../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../services/planningInputService` | `ObservedPlanningInput` | Specifier | compiler-dependent |
| `../services/planningInputService` | `planningInputService` | — | compiler-dependent |
| `../services/projectService` | `projectService` | — | compiler-dependent |
| `../services/releaseService` | `releaseService` | — | compiler-dependent |
| `../types/project` | `Project`, `ProjectHealth`, `ProjectMilestone`, `ProjectMilestoneCreateRequest`, `ProjectMilestoneStatus`, `ProjectMilestoneTaskGroup`, `ProjectMilestoneUpdateRequest`, `ProjectStatus`, `ProjectTargetDateRisk`, `ProjectUpdateEntry`, `ProjectUpdateFreshness` | Declaration | erased |
| `../types/release` | `Release`, `ReleaseStatus` | Declaration | erased |
| `../types/task` | `Task` | Declaration | erased |
| `../utils/apiError` | `normalizeApiError`, `getApiErrorMessage`, `getApiErrorStatus` | — | compiler-dependent |
| `../utils/formatDate` | `formatDate`, `formatDateTime` | — | compiler-dependent |
| `../utils/teamMemberLabels` | `formatPortfolioOwnerLabel` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `Activity`, `AlertTriangle`, `ArrowDown`, `ArrowUp`, `CalendarDays`, `CheckCircle2`, `ChevronRight`, `Edit`, `FolderOpen`, `History`, `MessageSquare`, `Package`, `Plus`, `Send`, `Target`, `Trash2`, `User`, `XCircle` | — | compiler-dependent |
| `react` | `FormEvent` | Declaration | erased |
| `react` | `useEffect`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link`, `useNavigate`, `useParams`, `useSearchParams` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |
| Constants | `PROJECT_TASK_PREVIEW`, `t`, `projectStatusLabelKeys`, `milestoneStatusLabelKeys`, `healthLabelKeys`, `riskLabelKeys`, `updateFreshnessLabelKeys`, `releaseStatusLabelKeys`, `textareaClassName` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/pages/ProjectDetailPage.tsx"]
    n1 --> n0
    click n1 "../modules/ProjectDetailPage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `frontend` (27) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 6 | 0 |

> All 27 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ProjectUpdateFormState](../entities/ProjectUpdateFormState.md) | Type alias | 157 | <pre><code>&#123;&#10;    health&#58; ProjectHealth&#59;&#10;    summary&#58; string&#59;&#10;    progress&#95;text&#58; string&#59;&#10;    risks&#95;text&#58; string&#59;&#10;    decisions&#95;text&#58; string&#59;&#10;    next&#95;steps&#95;text&#58; string&#59;&#10;&#125;</code></pre> | — |
| [ProjectUpdateFormStore](../entities/ProjectUpdateFormStore.md) | Type alias | 166 | <pre><code>&#123;&#10;    projectId&#58; number &#124; null&#59;&#10;    form&#58; ProjectUpdateFormState&#59;&#10;&#125;</code></pre> | — |
| [ProjectUpdateErrorStore](../entities/ProjectUpdateErrorStore.md) | Type alias | 171 | <pre><code>&#123;&#10;    projectId&#58; number &#124; null&#59;&#10;    message&#58; string &#124; null&#59;&#10;&#125;</code></pre> | — |
| [MilestoneFormState](../entities/MilestoneFormState.md) | Type alias | 176 | <pre><code>&#123;&#10;    name&#58; string&#59;&#10;    description&#58; string&#59;&#10;    target&#95;date&#58; string&#59;&#10;    completed&#95;at&#58; string&#59;&#10;    sort&#95;order&#58; string&#59;&#10;    status&#58; ProjectMilestoneStatus&#59;&#10;&#125;</code></pre> | — |
| [MilestoneEditorState](../entities/MilestoneEditorState.md) | Type alias | 185 | <pre><code>&#123;&#10;    mode&#58; &#39;create&#39; &#124; &#39;edit&#39;&#59;&#10;    milestone&#58; ProjectMilestone &#124; null&#59;&#10;    form&#58; MilestoneFormState&#59;&#10;    error&#58; string &#124; null&#59;&#10;&#125;</code></pre> | — |
