# ProjectIterationsSection Module

**Path:** `frontend/src/components/projects/ProjectIterationsSection.tsx`

## Description

_Auto-generated from `frontend/src/components/projects/ProjectIterationsSection.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../features/usePlanningObservation` | `usePlanningObservation` |
| `../../services/iterationService` | `iterationService` |
| `../../services/planningInputService` | `planningInputService`, `ObservedRevisions` |
| `../../types/iteration` | `Iteration` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../../utils/formatDate` | `formatDate` |
| `../common/Button` | `Button` |
| `../common/ConfirmDialog` | `ConfirmDialog` |
| `../common/Modal` | `Modal` |
| `../feedback/QueryState` | `QueryErrorState` |
| `../iteration/IterationForm` | `IterationForm` |
| `../ui` | `InlineEmptyState`, `SectionCard` |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` |
| `lucide-react` | `CalendarDays`, `Link2`, `Pencil`, `Plus`, `Unlink` |
| `react` | `useMemo`, `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ProjectIterationsSection` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/projects/ProjectIterationsSection.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/ProjectIterationsSection.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (1) |
| Outbound | `frontend` (12) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

> All 13 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ProjectIterationsSectionProps](../entities/ProjectIterationsSectionProps.md) | Class | 18 | — | — |
| [IterationEditorState](../entities/IterationEditorState.md) | Type alias | 25 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ProjectIterationsSection` | `({     projectId,     projectName,     iterations,     isLoading, }: ProjectIterationsSectionProps)` | — | — |
