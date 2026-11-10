# ProjectIterationsSection Module

**Path:** `frontend/src/components/projects/ProjectIterationsSection.tsx`

## Description

_Auto-generated from `frontend/src/components/projects/ProjectIterationsSection.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/usePlanningObservation` | `usePlanningObservation` | — | compiler-dependent |
| `../../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../../services/planningInputService` | `ObservedRevisions` | Specifier | compiler-dependent |
| `../../services/planningInputService` | `planningInputService` | — | compiler-dependent |
| `../../types/iteration` | `Iteration` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../../utils/formatDate` | `formatDate` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/ConfirmDialog` | `ConfirmDialog` | — | compiler-dependent |
| `../common/Modal` | `Modal` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `../iteration/IterationForm` | `IterationForm` | — | compiler-dependent |
| `../ui` | `InlineEmptyState`, `SectionCard` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `lucide-react` | `CalendarDays`, `Link2`, `Pencil`, `Plus`, `Unlink` | — | compiler-dependent |
| `react` | `useMemo`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ProjectIterationsSection` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

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
| [ProjectIterationsSectionProps](../entities/ProjectIterationsSectionProps.md) | Interface | 18 | — | — |
| [IterationEditorState](../entities/IterationEditorState.md) | Type alias | 25 | <pre><code>&#124; &#123; mode&#58; &#39;create&#39;&#59; iteration&#58; null &#125;&#10;    &#124; &#123; mode&#58; &#39;edit&#39;&#59; iteration&#58; Iteration &#125;</code></pre> | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ProjectIterationsSection` | <pre><code>&#40;&#123;&#10;    projectId&#44;&#10;    projectName&#44;&#10;    iterations&#44;&#10;    isLoading&#44;&#10;&#125;&#58; ProjectIterationsSectionProps&#41;</code></pre> | — | — |
