# RoadmapPage Module

**Path:** `frontend/src/pages/RoadmapPage.tsx`

## Description

_Auto-generated from `frontend/src/pages/RoadmapPage.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../components/common/Button` | `Button` |
| `../components/feedback/QueryState` | `QueryErrorState`, `QueryStaleState` |
| `../components/planning/PlanningWorkbenchFrame` | `PlanningWorkbenchFrame` |
| `../components/projects/projectStatusStyles` | `projectStatusBadgeClassName` |
| `../components/ui` | `FormGrid`, `InlineEmptyState`, `InlineField`, `SlideOverDrawer` |
| `../i18n/dateLocale` | `dateFnsLocale` |
| `../i18n/i18n` | `i18n` |
| `../services/projectService` | `projectService` |
| `../types/project` | `Initiative`, `Project`, `ProjectHealth`, `ProjectMilestone`, `ProjectMilestoneStatus`, `ProjectStatus` |
| `../utils/formatDate` | `formatDate` |
| `../utils/teamMemberLabels` | `formatPortfolioOwnerLabel` |
| `@tanstack/react-query` | `useInfiniteQuery`, `useQuery` |
| `clsx` | `clsx` |
| `date-fns` | `addDays`, `compareAsc`, `differenceInCalendarDays`, `eachMonthOfInterval`, `format`, `parseISO`, `startOfMonth` |
| `lucide-react` | `FolderOpen`, `ListFilter`, `Map`, `RotateCcw`, `X` |
| `react` | `useEffect`, `useId`, `useMemo`, `useState` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `Link` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |
| Constants | `t`, `projectStatusLabelKeys`, `projectHealthLabelKeys`, `milestoneStatusLabelKeys` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/pages/RoadmapPage.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/RoadmapPage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (1) |
| Outbound | `frontend` (11) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 7 | 0 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [RoadmapMarker](../entities/RoadmapMarker.md) | Type alias | 41 | — | — |
| [RoadmapRow](../entities/RoadmapRow.md) | Type alias | 46 | — | — |
| [DateRange](../entities/DateRange.md) | Type alias | 56 | — | — |
| [InitiativeGroupInfo](../entities/InitiativeGroupInfo.md) | Type alias | 61 | — | — |
| [RoadmapGroup](../entities/RoadmapGroup.md) | Type alias | 66 | — | — |
| [RoadmapFilterDescriptor](../entities/RoadmapFilterDescriptor.md) | Type alias | 72 | — | — |
