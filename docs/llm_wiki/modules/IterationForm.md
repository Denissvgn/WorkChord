# IterationForm Module

**Path:** `frontend/src/components/iteration/IterationForm.tsx`

## Description

_Auto-generated from `frontend/src/components/iteration/IterationForm.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../../services/planningInputService` | `ObservedRevisions` | Declaration | erased |
| `../../services/projectService` | `projectService` | — | compiler-dependent |
| `../../store/iterationStore` | `useIterationStore` | — | compiler-dependent |
| `../../types/iteration` | `Iteration`, `IterationCreate`, `IterationSeriesCreate`, `IterationUpdate` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../../utils/formatDate` | `formatDate` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/CollapsibleSection` | `CollapsibleSection` | — | compiler-dependent |
| `../common/Input` | `Input` | — | compiler-dependent |
| `../planning/PlanningInputBoundary` | `PlanningInputBoundary` | — | compiler-dependent |
| `../tasks/useDraftDismissal` | `useActiveMount` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `lucide-react` | `CalendarRange`, `ListChecks`, `Repeat`, `Save` | — | compiler-dependent |
| `react` | `ReactNode` | Declaration | erased |
| `react` | `useEffect`, `useMemo`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `IterationForm` |
| Constants | `MAX_SERIES_ITERATIONS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

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
| [IterationFormProps](../entities/IterationFormProps.md) | Interface | 24 | — | — |
| [EditorMode](../entities/EditorMode.md) | Type alias | 36 | `'single' \| 'series'` | — |
| [StopMode](../entities/StopMode.md) | Type alias | 37 | `'count' \| 'until_date'` | — |
| [SingleDraft](../entities/SingleDraft.md) | Type alias | 39 | <pre><code>&#123;&#10;    name&#58; string&#59;&#10;    project&#95;id&#58; string&#59;&#10;    start&#95;date&#58; string&#59;&#10;    end&#95;date&#58; string&#59;&#10;    manager&#95;email&#58; string&#59;&#10;&#125;</code></pre> | — |
| [SeriesDraft](../entities/SeriesDraft.md) | Type alias | 47 | <pre><code>&#123;&#10;    base&#95;name&#58; string&#59;&#10;    project&#95;id&#58; string&#59;&#10;    start&#95;date&#58; string&#59;&#10;    duration&#95;days&#58; number&#59;&#10;    stop&#95;mode&#58; StopMode&#59;&#10;    count&#58; number&#59;&#10;    until&#95;date&#58; string&#59;&#10;    manager&#95;email&#58; string&#59;&#10;&#125;</code></pre> | — |
| [EditorBaseline](../entities/EditorBaseline.md) | Type alias | 58 | <pre><code>&#123;&#10;    mode&#58; EditorMode&#59;&#10;    singleDraft&#58; SingleDraft&#59;&#10;    seriesDraft&#58; SeriesDraft&#59;&#10;&#125;</code></pre> | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `IterationForm` | `(props: IterationFormProps)` | — | — |
