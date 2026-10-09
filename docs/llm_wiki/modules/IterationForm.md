# IterationForm Module

**Path:** `frontend/src/components/iteration/IterationForm.tsx`

## Description

_Auto-generated from `frontend/src/components/iteration/IterationForm.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/iterationService` | `iterationService` |
| `../../services/planningInputService` | `ObservedRevisions` |
| `../../services/projectService` | `projectService` |
| `../../store/iterationStore` | `useIterationStore` |
| `../../types/iteration` | `Iteration`, `IterationCreate`, `IterationSeriesCreate`, `IterationUpdate` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../../utils/formatDate` | `formatDate` |
| `../common/Button` | `Button` |
| `../common/CollapsibleSection` | `CollapsibleSection` |
| `../common/Input` | `Input` |
| `../planning/PlanningInputBoundary` | `PlanningInputBoundary` |
| `../tasks/useDraftDismissal` | `useActiveMount` |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` |
| `lucide-react` | `CalendarRange`, `ListChecks`, `Repeat`, `Save` |
| `react` | `ReactNode`, `useEffect`, `useMemo`, `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `IterationForm` |
| Constants | `MAX_SERIES_ITERATIONS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/iteration/IterationForm.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/IterationForm.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (3) |
| Outbound | `frontend` (12) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

> All 15 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [IterationFormProps](../entities/IterationFormProps.md) | Class | 24 | — | — |
| [EditorMode](../entities/EditorMode.md) | Type alias | 36 | — | — |
| [StopMode](../entities/StopMode.md) | Type alias | 37 | — | — |
| [SingleDraft](../entities/SingleDraft.md) | Type alias | 39 | — | — |
| [SeriesDraft](../entities/SeriesDraft.md) | Type alias | 47 | — | — |
| [EditorBaseline](../entities/EditorBaseline.md) | Type alias | 58 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `IterationForm` | `(props: IterationFormProps)` | — | — |
