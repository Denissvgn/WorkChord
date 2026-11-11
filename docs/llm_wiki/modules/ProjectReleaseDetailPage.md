# ProjectReleaseDetailPage Module

**Path:** `frontend/src/pages/ProjectReleaseDetailPage.tsx`

## Description

_Auto-generated from `frontend/src/pages/ProjectReleaseDetailPage.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/common/Button` | `Button` | — | compiler-dependent |
| `../components/common/Modal` | `Modal` | — | compiler-dependent |
| `../components/common/useConfirmDialog` | `useConfirmDialog` | — | compiler-dependent |
| `../components/feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `../components/layout/Breadcrumbs` | `Breadcrumbs` | — | compiler-dependent |
| `../components/releases/ReleaseForm` | `ReleaseForm` | — | compiler-dependent |
| `../components/tasks/WorkMetricsLine` | `WorkMetricsLine` | — | compiler-dependent |
| `../components/ui` | `MetricGrid`, `PageHeader`, `PageLayout` | — | compiler-dependent |
| `../components/ui/tone` | `isTaskStatus`, `pillToneClassName`, `STATUS_TONE`, `statusTextClassName` | — | compiler-dependent |
| `../features/mutationFeedback` | `MutationFeedbackMeta` | Declaration | erased |
| `../services/projectService` | `projectService` | — | compiler-dependent |
| `../services/releaseService` | `releaseService` | — | compiler-dependent |
| `../types/release` | `Release`, `ReleaseStatus`, `ReleaseTaskSummary` | Declaration | erased |
| `../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../utils/formatDate` | `formatDate`, `formatDateTime` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `CalendarDays`, `CheckCircle2`, `Clock`, `Edit`, `FolderOpen`, `Package`, `Tag` | — | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `useNavigate`, `useParams` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |
| Constants | `releaseStatusLabelKeys` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/pages/ProjectReleaseDetailPage.tsx"]
    n1 --> n0
    click n1 "../modules/ProjectReleaseDetailPage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `frontend` (15) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 6 | 0 |

> All 15 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.
