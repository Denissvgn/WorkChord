# ProjectIterationsSection Module

**Path:** `frontend/src/components/projects/ProjectIterationsSection.tsx`

## Description

_Auto-generated from `frontend/src/components/projects/ProjectIterationsSection.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/iterationService` | `iterationService` |
| `../../types/iteration` | `Iteration` |
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
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/ConfirmDialog.tsx"]
    n2["frontend/src/components/common/Modal.tsx"]
    n3["frontend/src/components/feedback/QueryState.tsx"]
    n4["frontend/src/components/iteration/IterationForm.tsx"]
    n5["frontend/src/components/projects/ProjectIterationsSection.tsx"]
    n6["frontend/src/components/ui/index.ts"]
    n7["frontend/src/pages/ProjectDetailPage.tsx"]
    n8["frontend/src/services/iterationService.ts"]
    n9["frontend/src/types/iteration.ts"]
    n10["frontend/src/utils/formatDate.ts"]
    n1 --> n0
    n1 --> n2
    n3 --> n0
    n4 --> n0
    n4 --> n8
    n4 --> n9
    n4 --> n10
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n4
    n5 --> n6
    n5 --> n8
    n5 --> n9
    n5 --> n10
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n5
    n7 --> n6
    n7 --> n10
    n8 --> n9
    click n0 "../modules/Button.md"
    click n1 "../modules/ConfirmDialog.md"
    click n2 "../modules/Modal.md"
    click n3 "../modules/QueryState.md"
    click n4 "../modules/IterationForm.md"
    click n5 "../modules/ProjectIterationsSection.md"
    click n6 "../modules/index.md"
    click n7 "../modules/ProjectDetailPage.md"
    click n8 "../modules/iterationService.md"
    click n9 "../modules/types_iteration.md"
    click n10 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [ConfirmDialog](../modules/ConfirmDialog.md) |
| Outbound | [Modal](../modules/Modal.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [IterationForm](../modules/IterationForm.md) |
| Outbound | [index](../modules/index.md) |
| Outbound | [iterationService](../modules/iterationService.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |
| Outbound | [formatDate](../modules/formatDate.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ProjectIterationsSectionProps](../entities/ProjectIterationsSectionProps.md) | Class | 15 | — | — |
| [IterationEditorState](../entities/IterationEditorState.md) | Type alias | 22 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ProjectIterationsSection` | `({     projectId,     projectName,     iterations,     isLoading, }: ProjectIterationsSectionProps)` | — | — |
