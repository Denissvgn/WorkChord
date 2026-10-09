# IterationsPage Module

**Path:** `frontend/src/pages/IterationsPage.tsx`

## Description

_Auto-generated from `frontend/src/pages/IterationsPage.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../components/iteration/IterationForm` | `IterationForm` |
| `../components/iteration/IterationImportDialog` | `IterationImportDialog` |
| `../components/iteration/IterationList` | `IterationList` |
| `../components/planning/PlanReturnBar` | `PlanReturnBar` |
| `../components/ui` | `PageHeader`, `PageLayout` |
| `../types/iteration` | `Iteration` |
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
    n0["frontend/src/components/iteration/IterationForm.tsx"]
    n1["frontend/src/components/iteration/IterationImportDialog.tsx"]
    n2["frontend/src/components/iteration/IterationList.tsx"]
    n3["frontend/src/components/planning/PlanReturnBar.tsx"]
    n4["frontend/src/components/ui/index.ts"]
    n5["frontend/src/pages/IterationsPage.tsx"]
    n6["frontend/src/types/iteration.ts"]
    n0 --> n6
    n2 --> n1
    n2 --> n6
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n4
    n5 --> n6
    click n0 "../modules/IterationForm.md"
    click n1 "../modules/IterationImportDialog.md"
    click n2 "../modules/IterationList.md"
    click n3 "../modules/PlanReturnBar.md"
    click n4 "../modules/index.md"
    click n5 "../modules/IterationsPage.md"
    click n6 "../modules/types_iteration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [IterationForm](../modules/IterationForm.md) |
| Outbound | [IterationImportDialog](../modules/IterationImportDialog.md) |
| Outbound | [IterationList](../modules/IterationList.md) |
| Outbound | [PlanReturnBar](../modules/PlanReturnBar.md) |
| Outbound | [index](../modules/index.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
