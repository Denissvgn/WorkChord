# ProjectDetailPage Module

**Path:** `frontend/src/pages/ProjectDetailPage.tsx`

## Description

_Auto-generated from `frontend/src/pages/ProjectDetailPage.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../components/common/Button` | `Button` |
| `../components/common/ConfirmDialog` | `ConfirmDialog` |
| `../components/common/Input` | `RequiredIndicator` |
| `../components/common/Modal` | `Modal` |
| `../components/feedback/QueryState` | `QueryErrorState` |
| `../components/layout/Breadcrumbs` | `Breadcrumbs` |
| `../components/projects/ProjectForm` | `ProjectForm` |
| `../components/projects/ProjectIterationsSection` | `ProjectIterationsSection` |
| `../components/projects/ProjectTaskTree` | `ProjectTaskTree` |
| `../components/projects/projectStatusStyles` | `projectStatusBadgeClassName`, `projectStatusPillClassName` |
| `../components/releases/ReleaseForm` | `ReleaseForm` |
| `../components/requestSources/RequestSourceLinksPanel` | `RequestSourceLinksPanel` |
| `../components/tasks/GuardedTaskModal` | `GuardedTaskModal` |
| `../components/tasks/WorkMetricsLine` | `WorkMetricsLine` |
| `../components/ui` | `InlineEmptyState`, `OverflowMenu`, `MetricGrid`, `PageHeader`, `PageLayout`, `Pill`, `SectionCard`, `SlideOverDrawer`, `StatusSegmentStrip`, `StickyRail` |
| `../components/ui/tone` | `STATUS_TONE` |
| `../i18n/i18n` | `i18n` |
| `../services/projectService` | `projectService` |
| `../services/releaseService` | `releaseService` |
| `../types/project` | `ProjectHealth`, `ProjectMilestone`, `ProjectMilestoneCreateRequest`, `ProjectMilestoneStatus`, `ProjectMilestoneTaskGroup`, `ProjectMilestoneUpdateRequest`, `ProjectStatus`, `ProjectTargetDateRisk`, `ProjectUpdateEntry`, `ProjectUpdateFreshness` |
| `../types/release` | `Release`, `ReleaseStatus` |
| `../utils/apiError` | `getApiErrorMessage`, `getApiErrorStatus` |
| `../utils/formatDate` | `formatDate`, `formatDateTime` |
| `../utils/teamMemberLabels` | `formatPortfolioOwnerLabel` |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` |
| `clsx` | `clsx` |
| `lucide-react` | `Activity`, `AlertTriangle`, `ArrowDown`, `ArrowUp`, `CalendarDays`, `CheckCircle2`, `ChevronRight`, `Edit`, `FolderOpen`, `History`, `MessageSquare`, `Package`, `Plus`, `Send`, `Target`, `Trash2`, `User`, `XCircle` |
| `react` | `useState`, `FormEvent` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `Link`, `useNavigate`, `useParams` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |
| Constants | `t`, `projectStatusLabelKeys`, `milestoneStatusLabelKeys`, `healthLabelKeys`, `riskLabelKeys`, `updateFreshnessLabelKeys`, `releaseStatusLabelKeys`, `textareaClassName` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
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
| Outbound | `frontend` (24) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 6 | 0 |

> All 24 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ProjectUpdateFormState](../entities/ProjectUpdateFormState.md) | Type alias | 151 | — | — |
| [ProjectUpdateFormStore](../entities/ProjectUpdateFormStore.md) | Type alias | 160 | — | — |
| [ProjectUpdateErrorStore](../entities/ProjectUpdateErrorStore.md) | Type alias | 165 | — | — |
| [MilestoneFormState](../entities/MilestoneFormState.md) | Type alias | 170 | — | — |
| [MilestoneEditorState](../entities/MilestoneEditorState.md) | Type alias | 179 | — | — |
