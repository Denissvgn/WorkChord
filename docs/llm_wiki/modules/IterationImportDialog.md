# IterationImportDialog Module

**Path:** `frontend/src/components/iteration/IterationImportDialog.tsx`

## Description

JSON import confirms the retained file against its original complete observation. Conflicts retain the file and require an explicit current-input review to change context; no save-time read or automatic retry occurs.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/exportService` | `exportService` | — | compiler-dependent |
| `../../services/planningInputService` | `ObservedRevisions` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/DisabledReason` | `DisabledReason` | — | compiler-dependent |
| `../common/Modal` | `Modal` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `../tasks/useDraftDismissal` | `useActiveMount` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `react` | `useId` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `IterationImportDialog` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/DisabledReason.tsx"]
    n2["frontend/src/components/common/Modal.tsx"]
    n3["frontend/src/components/feedback/QueryState.tsx"]
    n4["frontend/src/components/iteration/IterationImportDialog.tsx"]
    n5["frontend/src/components/iteration/IterationList.tsx"]
    n6["frontend/src/components/tasks/useDraftDismissal.ts"]
    n7["frontend/src/pages/IterationsPage.tsx"]
    n8["frontend/src/services/exportService.ts"]
    n9["frontend/src/services/planningInputService.ts"]
    n10["frontend/src/utils/apiError.ts"]
    n3 --> n0
    n3 --> n10
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n6
    n4 --> n8
    n4 --> n9
    n4 --> n10
    n5 --> n0
    n5 --> n4
    n5 --> n8
    n5 --> n9
    n5 --> n10
    n7 --> n4
    n7 --> n5
    n8 --> n9
    click n0 "../modules/Button.md"
    click n1 "../modules/DisabledReason.md"
    click n2 "../modules/Modal.md"
    click n3 "../modules/QueryState.md"
    click n4 "../modules/IterationImportDialog.md"
    click n5 "../modules/IterationList.md"
    click n6 "../modules/useDraftDismissal.md"
    click n7 "../modules/IterationsPage.md"
    click n8 "../modules/exportService.md"
    click n9 "../modules/planningInputService.md"
    click n10 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [IterationList](../modules/IterationList.md) |
| Inbound | [IterationsPage](../modules/IterationsPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [DisabledReason](../modules/DisabledReason.md) |
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