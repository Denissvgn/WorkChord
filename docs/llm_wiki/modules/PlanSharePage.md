# PlanSharePage Module

**Path:** `frontend/src/pages/PlanSharePage.tsx`

## Description

_Auto-generated from `frontend/src/pages/PlanSharePage.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../components/common/Button` | `Button` |
| `../components/feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` |
| `../components/feedback/toast` | `useToast` |
| `../components/ui` | `PageHeader`, `PageLayout` |
| `../services/planShareService` | `planShareService`, `PlanShareTask` |
| `../utils/copyText` | `copyText` |
| `../utils/formatDate` | `formatDate`, `formatDateTime` |
| `@tanstack/react-query` | `useQuery` |
| `lucide-react` | `CalendarDays`, `CheckCircle2`, `Copy`, `ExternalLink`, `ListChecks`, `Users` |
| `react` | `useMemo` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `Link`, `useParams` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/components/feedback/toast.ts"]
    n3["frontend/src/components/ui/index.ts"]
    n4["frontend/src/pages/PlanSharePage.test.tsx"]
    n5["frontend/src/pages/PlanSharePage.tsx"]
    n6["frontend/src/services/planShareService.ts"]
    n7["frontend/src/utils/copyText.ts"]
    n8["frontend/src/utils/formatDate.ts"]
    n1 --> n0
    n4 --> n5
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n6
    n5 --> n7
    n5 --> n8
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/toast.md"
    click n3 "../modules/index.md"
    click n4 "../modules/PlanSharePage.test.md"
    click n5 "../modules/PlanSharePage.md"
    click n6 "../modules/planShareService.md"
    click n7 "../modules/copyText.md"
    click n8 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PlanSharePage.test](../modules/PlanSharePage.test.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [toast](../modules/toast.md) |
| Outbound | [index](../modules/index.md) |
| Outbound | [planShareService](../modules/planShareService.md) |
| Outbound | [copyText](../modules/copyText.md) |
| Outbound | [formatDate](../modules/formatDate.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |
