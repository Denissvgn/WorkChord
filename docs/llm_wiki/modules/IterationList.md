# IterationList Module

**Path:** `frontend/src/components/iteration/IterationList.tsx`

## Description

_Auto-generated from `frontend/src/components/iteration/IterationList.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/exportService` | `exportService` |
| `../../services/iterationService` | `iterationService` |
| `../../services/planningInputService` | `planningInputService`, `ObservedRevisions` |
| `../../store/iterationStore` | `useIterationStore` |
| `../../types/iteration` | `Iteration` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../../utils/formatDate` | `formatDate` |
| `../common/Button` | `Button` |
| `../common/ConfirmDialog` | `ConfirmDialog` |
| `../feedback/toast` | `useToast` |
| `./IterationImportDialog` | `IterationImportDialog` |
| `@tanstack/react-query` | `useQuery`, `useMutation`, `useQueryClient` |
| `lucide-react` | `Calendar`, `Trash2`, `ArrowRight`, `Download`, `Upload`, `FolderOpen` |
| `react` | `useState`, `useRef` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `Link` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `IterationList` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/iteration/IterationList.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/IterationList.md"
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
| typescript | 5 | 0 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [IterationListProps](../entities/IterationListProps.md) | Class | 18 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `IterationList` | `({ onEdit }: IterationListProps)` | — | — |
