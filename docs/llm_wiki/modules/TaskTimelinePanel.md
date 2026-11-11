# TaskTimelinePanel Module

**Path:** `frontend/src/components/tasks/TaskTimelinePanel.tsx`

## Description

Merged history uses explicit bounded continuation. External-link read failures hide cached private links and their controls while retaining error/retry feedback; prior successful data does not imply current access.

_Auto-generated from `frontend/src/components/tasks/TaskTimelinePanel.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../types/task` | `ExternalLink`, `Task` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../../utils/formatDate` | `formatDateTime` | — | compiler-dependent |
| `../../utils/safeUrl` | `safeExternalHref` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `../requestSources/RequestSourceLinksPanel` | `RequestSourceLinksPanel` | — | compiler-dependent |
| `@tanstack/react-query` | `useInfiniteQuery`, `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `Bot`, `CircleDot`, `GitBranch`, `History`, `Link`, `Plus`, `RefreshCw`, `Trash2`, `X` | — | compiler-dependent |
| `react` | `KeyboardEvent` | Specifier | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskTimelinePanel` |
| Constants | `t`, `itemLabels`, `githubUrlPattern` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/feedback/QueryState.tsx"]
    n1["frontend/src/components/requestSources/RequestSourceLinksPanel.tsx"]
    n2["frontend/src/components/tasks/TaskForm.tsx"]
    n3["frontend/src/components/tasks/TaskReadView.tsx"]
    n4["frontend/src/components/tasks/TaskTimelinePanel.test.tsx"]
    n5["frontend/src/components/tasks/TaskTimelinePanel.tsx"]
    n6["frontend/src/i18n/i18n.ts"]
    n7["frontend/src/services/taskService.ts"]
    n8["frontend/src/types/task.ts"]
    n9["frontend/src/utils/apiError.ts"]
    n10["frontend/src/utils/formatDate.ts"]
    n11["frontend/src/utils/safeUrl.ts"]
    n0 --> n9
    n1 --> n0
    n1 --> n6
    n1 --> n9
    n1 --> n11
    n2 --> n0
    n2 --> n5
    n2 --> n7
    n2 --> n8
    n2 --> n9
    n2 --> n10
    n3 --> n5
    n3 --> n7
    n3 --> n8
    n3 --> n9
    n3 --> n10
    n4 --> n5
    n4 --> n8
    n5 --> n0
    n5 --> n1
    n5 --> n6
    n5 --> n7
    n5 --> n8
    n5 --> n9
    n5 --> n10
    n5 --> n11
    n7 --> n8
    click n0 "../modules/QueryState.md"
    click n1 "../modules/RequestSourceLinksPanel.md"
    click n2 "../modules/TaskForm.md"
    click n3 "../modules/TaskReadView.md"
    click n4 "../modules/TaskTimelinePanel.test.md"
    click n5 "../modules/TaskTimelinePanel.md"
    click n6 "../modules/i18n.md"
    click n7 "../modules/taskService.md"
    click n8 "../modules/types_task.md"
    click n9 "../modules/apiError.md"
    click n10 "../modules/formatDate.md"
    click n11 "../modules/safeUrl.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TaskReadView](../modules/TaskReadView.md) |
| Inbound | [TaskTimelinePanel.test](../modules/TaskTimelinePanel.test.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [RequestSourceLinksPanel](../modules/RequestSourceLinksPanel.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [apiError](../modules/apiError.md) |
| Outbound | [formatDate](../modules/formatDate.md) |
| Outbound | [safeUrl](../modules/safeUrl.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskTimelinePanelProps](../entities/TaskTimelinePanelProps.md) | Interface | 17 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskTimelinePanel` | `({ task }: TaskTimelinePanelProps)` | — | — |