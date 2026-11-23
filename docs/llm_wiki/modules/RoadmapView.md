# RoadmapView Module

**Path:** `frontend/src/components/projects/RoadmapView.tsx`

## Description

The roadmap is a view in Projects. It builds a project’s displayed span from its dates and dated milestones and shows unscheduled work separately. Following a project or milestone opens the corresponding project context.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/useLiveWindow` | `useLiveWindow` | — | compiler-dependent |
| `../../i18n/dateLocale` | `dateFnsLocale` | — | compiler-dependent |
| `../../services/projectService` | `projectService` | — | compiler-dependent |
| `../../types/project` | `Initiative`, `Project`, `ProjectHealth`, `ProjectMilestone`, `ProjectMilestoneStatus`, `ProjectStatus` | Declaration | erased |
| `../../utils/formatDate` | `formatDate` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../feedback/LiveWindowStatus` | `LiveWindowStatus` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryStaleState` | — | compiler-dependent |
| `../ui` | `InlineEmptyState` | — | compiler-dependent |
| `./AddMilestoneModal` | `AddMilestoneModal` | — | compiler-dependent |
| `./InitiativeGroupHeader` | `InitiativeGroupHeader` | — | compiler-dependent |
| `./SetDatesPopover` | `SetDatesPopover` | — | compiler-dependent |
| `./projectPortfolio` | `InitiativeGroup` | Specifier | compiler-dependent |
| `./projectPortfolio` | `groupByInitiative` | — | compiler-dependent |
| `./projectStatusStyles` | `projectHealthBadgeClassName`, `projectStatusBadgeClassName` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `date-fns` | `addDays`, `compareAsc`, `differenceInCalendarDays`, `eachMonthOfInterval`, `format`, `parseISO`, `startOfMonth` | — | compiler-dependent |
| `lucide-react` | `Map`, `Plus` | — | compiler-dependent |
| `react` | `useId`, `useMemo`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `RoadmapView` |
| Constants | `projectStatusLabelKeys`, `projectHealthLabelKeys`, `milestoneStatusLabelKeys`, `GRID_COLUMNS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/projects/RoadmapView.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/RoadmapView.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (3) |
| Outbound | `frontend` (14) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 6 | 0 |

> All 17 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [RoadmapMarker](../entities/RoadmapMarker.md) | Type alias | 37 | <pre><code>&#123;&#10;    milestone&#58; ProjectMilestone&#59;&#10;    date&#58; Date&#59;&#10;&#125;</code></pre> | — |
| [RoadmapRow](../entities/RoadmapRow.md) | Type alias | 42 | <pre><code>&#123;&#10;    project&#58; Project&#59;&#10;    milestones&#58; ProjectMilestone&#91;&#93;&#59;&#10;    markers&#58; RoadmapMarker&#91;&#93;&#59;&#10;    startDate&#58; Date &#124; null&#59;&#10;    endDate&#58; Date &#124; null&#59;&#10;    spanSource&#58; &#39;project&#39; &#124; &#39;single&#45;project&#45;date&#39; &#124; &#39;milestones&#39; &#124; &#39;none&#39;&#59;&#10;    &#47;&#42;&#42; Nothing to draw&#58; no project dates and no dated milestones&#46; &#42;&#47;&#10;    isUnscheduled&#58; boolean&#59;&#10;    &#47;&#42;&#42; The project has neither a start nor a target date&#44; even if its milestones give it a span&#46; &#42;&#47;&#10;    needsDates&#58; boolean&#59;&#10;&#125;</code></pre> | — |
| [DateRange](../entities/DateRange.md) | Type alias | 55 | <pre><code>&#123;&#10;    start&#58; Date&#59;&#10;    end&#58; Date&#59;&#10;&#125;</code></pre> | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `RoadmapView` | <pre><code>&#40;&#123;&#10;    projects&#44;&#10;    initiatives&#44;&#10;    includeEmptyGroups&#44;&#10;    window&#58; timelineWindow&#44;&#10;    onResetWindow&#44;&#10;    onEditInitiative&#44;&#10;    onDeleteInitiative&#44;&#10;&#125;&#58; &#123;&#10;    &#47;&#42;&#42; The projects left after the page&#39;s search and filters&#46; &#42;&#47;&#10;    projects&#58; Project&#91;&#93;&#59;&#10;    initiatives&#58; Initiative&#91;&#93;&#59;&#10;    includeEmptyGroups&#58; boolean&#59;&#10;    &#47;&#42;&#42; The window set by a preset&#44; as &#96;yyyy&#45;MM&#45;dd&#96;&#59; empty values fit the projects&#46; &#42;&#47;&#10;    window&#58; &#123; from&#58; string&#59; to&#58; string &#125;&#59;&#10;    onResetWindow&#58; &#40;&#41; &#61;&#62; void&#59;&#10;    onEditInitiative&#58; &#40;initiativeId&#58; number&#41; &#61;&#62; void&#59;&#10;    onDeleteInitiative&#58; &#40;initiativeId&#58; number&#41; &#61;&#62; void&#59;&#10;&#125;&#41;</code></pre> | — | The Roadmap view of Projects: the filtered projects on one date axis, under |