# ProjectsPage Module

**Path:** `frontend/src/pages/ProjectsPage.tsx`

## Description

_Auto-generated from `frontend/src/pages/ProjectsPage.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/common/Button` | `Button` | — | compiler-dependent |
| `../components/common/Input` | `Input` | — | compiler-dependent |
| `../components/common/Modal` | `Modal` | — | compiler-dependent |
| `../components/common/useConfirmDialog` | `useConfirmDialog` | — | compiler-dependent |
| `../components/feedback/QueryState` | `QueryErrorState`, `QueryLoadingState`, `QueryStaleState` | — | compiler-dependent |
| `../components/projects/InitiativeForm` | `InitiativeForm` | — | compiler-dependent |
| `../components/projects/ProjectForm` | `ProjectForm` | — | compiler-dependent |
| `../components/projects/projectStatusStyles` | `projectStatusBadgeClassName` | — | compiler-dependent |
| `../components/ui` | `InlineEmptyState`, `OverflowMenu`, `PageHeader`, `PageLayout`, `TableFrame` | — | compiler-dependent |
| `../features/mutationFeedback` | `MutationFeedbackMeta` | Declaration | erased |
| `../features/mutationFeedback` | `feedbackMessage` | — | compiler-dependent |
| `../services/projectService` | `projectService` | — | compiler-dependent |
| `../services/savedViewService` | `savedViewService` | — | compiler-dependent |
| `../types/project` | `Initiative`, `Project`, `ProjectHealth`, `ProjectPortfolioSummary`, `ProjectStatus` | Declaration | erased |
| `../types/savedView` | `SavedView` | Declaration | erased |
| `../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../utils/formatDate` | `formatDate` | — | compiler-dependent |
| `../utils/teamMemberLabels` | `formatPortfolioOwnerLabel` | — | compiler-dependent |
| `../utils/workNumbers` | `formatEffortDays` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `AlertTriangle`, `ChevronDown`, `FolderOpen`, `LoaderCircle`, `Plus`, `Search`, `Target` | — | compiler-dependent |
| `react` | `useCallback`, `useEffect`, `useMemo`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link`, `useNavigate`, `useSearchParams` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |
| Constants | `projectStatusLabelKeys`, `projectHealthLabelKeys`, `riskLabelKeys`, `SORT_COLUMNS`, `RISK_ORDER` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/pages/ProjectsPage.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/ProjectsPage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (1) |
| Outbound | `frontend` (18) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 6 | 0 |

> All 19 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [SortKey](../entities/ProjectsPage_SortKey.md) | Type alias | 106 | `'name' \| 'status' \| 'owner' \| 'target' \| 'tasks' \| 'effort' \| 'signals'` | — |
