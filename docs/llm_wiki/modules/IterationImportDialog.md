# IterationImportDialog Module

**Path:** `frontend/src/components/iteration/IterationImportDialog.tsx`

## Description

JSON import confirms the retained file against its original complete observation. Conflicts retain the file and require an explicit current-input review to change context; no save-time read or automatic retry occurs.

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/exportService` | `exportService` |
| `../../services/planningInputService` | `ObservedRevisions` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../common/Button` | `Button` |
| `../common/Modal` | `Modal` |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` |
| `../tasks/useDraftDismissal` | `useActiveMount` |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` |
| `react` | `useId` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `IterationImportDialog` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Modal.tsx"]
    n2["frontend/src/components/feedback/QueryState.tsx"]
    n3["frontend/src/components/iteration/IterationImportDialog.tsx"]
    n4["frontend/src/components/iteration/IterationList.tsx"]
    n5["frontend/src/components/tasks/useDraftDismissal.ts"]
    n6["frontend/src/pages/IterationsPage.tsx"]
    n7["frontend/src/services/exportService.ts"]
    n8["frontend/src/services/planningInputService.ts"]
    n9["frontend/src/utils/apiError.ts"]
    n2 --> n0
    n2 --> n9
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n5
    n3 --> n7
    n3 --> n8
    n3 --> n9
    n4 --> n0
    n4 --> n3
    n4 --> n7
    n4 --> n8
    n4 --> n9
    n6 --> n3
    n6 --> n4
    n7 --> n8
    click n0 "../modules/Button.md"
    click n1 "../modules/Modal.md"
    click n2 "../modules/QueryState.md"
    click n3 "../modules/IterationImportDialog.md"
    click n4 "../modules/IterationList.md"
    click n5 "../modules/useDraftDismissal.md"
    click n6 "../modules/IterationsPage.md"
    click n7 "../modules/exportService.md"
    click n8 "../modules/planningInputService.md"
    click n9 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [IterationList](../modules/IterationList.md) |
| Inbound | [IterationsPage](../modules/IterationsPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Modal](../modules/Modal.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [useDraftDismissal](../modules/useDraftDismissal.md) |
| Outbound | [exportService](../modules/exportService.md) |
| Outbound | [planningInputService](../modules/planningInputService.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `IterationImportDialog` | `({ file, iterationId, onClose }: { file: File; iterationId?: number; onClose: () => void })` | — | — |
