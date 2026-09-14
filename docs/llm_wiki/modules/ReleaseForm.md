# ReleaseForm Module

**Path:** `frontend/src/components/releases/ReleaseForm.tsx`

## Description

_Auto-generated from `frontend/src/components/releases/ReleaseForm.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/projectService` | `projectService` |
| `../../services/releaseService` | `releaseService` |
| `../../types/release` | `Release`, `ReleaseCreateRequest`, `ReleaseStatus`, `ReleaseUpdateRequest` |
| `../../types/task` | `Task` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../common/Button` | `Button` |
| `../common/CollapsibleSection` | `CollapsibleSection` |
| `../feedback/QueryState` | `QueryErrorState` |
| `../ui/tone` | `pillToneClassName`, `STATUS_TONE` |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` |
| `clsx` | `clsx` |
| `lucide-react` | `Save` |
| `react` | `useMemo`, `useState`, `FormEvent` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ReleaseForm` |
| Constants | `releaseStatusOptions`, `textInputClassName` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/CollapsibleSection.tsx"]
    n2["frontend/src/components/feedback/QueryState.tsx"]
    n3["frontend/src/components/releases/ReleaseForm.tsx"]
    n4["frontend/src/components/ui/tone.ts"]
    n5["frontend/src/pages/ProjectDetailPage.tsx"]
    n6["frontend/src/pages/ProjectReleaseDetailPage.tsx"]
    n7["frontend/src/services/projectService.ts"]
    n8["frontend/src/services/releaseService.ts"]
    n9["frontend/src/types/release.ts"]
    n10["frontend/src/types/task.ts"]
    n11["frontend/src/utils/apiError.ts"]
    n2 --> n0
    n2 --> n11
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    n3 --> n7
    n3 --> n8
    n3 --> n9
    n3 --> n10
    n3 --> n11
    n4 --> n10
    n5 --> n0
    n5 --> n2
    n5 --> n3
    n5 --> n4
    n5 --> n7
    n5 --> n8
    n5 --> n9
    n5 --> n11
    n6 --> n0
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n6 --> n7
    n6 --> n8
    n6 --> n9
    n6 --> n11
    n7 --> n10
    n8 --> n9
    n9 --> n10
    click n0 "../modules/Button.md"
    click n1 "../modules/CollapsibleSection.md"
    click n2 "../modules/QueryState.md"
    click n3 "../modules/ReleaseForm.md"
    click n4 "../modules/tone.md"
    click n5 "../modules/ProjectDetailPage.md"
    click n6 "../modules/ProjectReleaseDetailPage.md"
    click n7 "../modules/projectService.md"
    click n8 "../modules/releaseService.md"
    click n9 "../modules/types_release.md"
    click n10 "../modules/types_task.md"
    click n11 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Inbound | [ProjectReleaseDetailPage](../modules/ProjectReleaseDetailPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [CollapsibleSection](../modules/CollapsibleSection.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [tone](../modules/tone.md) |
| Outbound | [projectService](../modules/projectService.md) |
| Outbound | [releaseService](../modules/releaseService.md) |
| Outbound | [types_release](../modules/types_release.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ReleaseFormProps](../entities/ReleaseFormProps.md) | Class | 22 | — | — |
| [FlattenedTask](../entities/ReleaseForm_FlattenedTask.md) | Type alias | 29 | — | — |
| [ReleaseFormState](../entities/ReleaseFormState.md) | Type alias | 34 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ReleaseForm` | `({     projectId,     initialData,     onSuccess,     onCancel, }: ReleaseFormProps)` | — | — |
