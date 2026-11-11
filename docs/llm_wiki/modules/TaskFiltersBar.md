# TaskFiltersBar Module

**Path:** `frontend/src/components/tasks/TaskFiltersBar.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskFiltersBar.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/planningMasters/planningTaskIssues` | `PlanningTaskIssue` | Declaration | erased |
| `../../i18n/seedDisplay` | `labelDisplay`, `labelGroupDisplay` | — | compiler-dependent |
| `../../services/labelService` | `labelService` | — | compiler-dependent |
| `../../services/projectService` | `projectService` | — | compiler-dependent |
| `../../services/teamService` | `teamService` | — | compiler-dependent |
| `../../utils/formatDate` | `formatDate` | — | compiler-dependent |
| `../../utils/taskFilterDefaults` | `defaultFilters` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `./TaskTextEditorModal` | `TaskTextEditorModal` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `lucide-react` | `ChevronDown`, `ChevronRight`, `X`, `FileText`, `XCircle` | — | compiler-dependent |
| `react` | `useId`, `useMemo`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskFilters`, `TaskFiltersBar` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/tasks/TaskFiltersBar.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/TaskFiltersBar.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (10) |
| Outbound | `frontend` (10) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

> All 19 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskFilters](../entities/TaskFilters.md) | Interface | 16 | — | — |
| [TaskFiltersBarProps](../entities/TaskFiltersBarProps.md) | Interface | 35 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskFiltersBar` | `({ iterationId, filters, onFiltersChange }: TaskFiltersBarProps)` | — | — |
