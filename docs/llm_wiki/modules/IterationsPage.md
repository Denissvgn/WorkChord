# IterationsPage Module

**Path:** `frontend/src/pages/IterationsPage.tsx`

## Description

_Auto-generated from `frontend/src/pages/IterationsPage.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../components/feedback/toast` | `useToast` |
| `../components/iteration/IterationForm` | `IterationForm` |
| `../components/iteration/IterationList` | `IterationList` |
| `../components/planning/PlanReturnBar` | `PlanReturnBar` |
| `../components/ui` | `PageHeader`, `PageLayout` |
| `../services/exportService` | `exportService` |
| `../types/iteration` | `Iteration` |
| `../utils/apiError` | `getApiErrorMessage` |
| `@tanstack/react-query` | `useQueryClient` |
| `react` | `useState`, `useRef` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/feedback/toast.ts"]
    n1["frontend/src/components/iteration/IterationForm.tsx"]
    n2["frontend/src/components/iteration/IterationList.tsx"]
    n3["frontend/src/components/planning/PlanReturnBar.tsx"]
    n4["frontend/src/components/ui/index.ts"]
    n5["frontend/src/pages/IterationsPage.tsx"]
    n6["frontend/src/services/exportService.ts"]
    n7["frontend/src/types/iteration.ts"]
    n8["frontend/src/utils/apiError.ts"]
    n1 --> n7
    n1 --> n8
    n2 --> n0
    n2 --> n6
    n2 --> n7
    n2 --> n8
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n4
    n5 --> n6
    n5 --> n7
    n5 --> n8
    click n0 "../modules/toast.md"
    click n1 "../modules/IterationForm.md"
    click n2 "../modules/IterationList.md"
    click n3 "../modules/PlanReturnBar.md"
    click n4 "../modules/index.md"
    click n5 "../modules/IterationsPage.md"
    click n6 "../modules/exportService.md"
    click n7 "../modules/types_iteration.md"
    click n8 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [toast](../modules/toast.md) |
| Outbound | [IterationForm](../modules/IterationForm.md) |
| Outbound | [IterationList](../modules/IterationList.md) |
| Outbound | [PlanReturnBar](../modules/PlanReturnBar.md) |
| Outbound | [index](../modules/index.md) |
| Outbound | [exportService](../modules/exportService.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
