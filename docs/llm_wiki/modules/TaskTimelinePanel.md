# TaskTimelinePanel Module

**Path:** `frontend/src/components/tasks/TaskTimelinePanel.tsx`

## Description

Merged history uses explicit bounded continuation. External-link read failures hide cached private links and their controls while retaining error/retry feedback; prior successful data does not imply current access.

_Auto-generated from `frontend/src/components/tasks/TaskTimelinePanel.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../i18n/i18n` | `i18n` |
| `../../services/taskService` | `taskService` |
| `../../types/task` | `ExternalLink`, `Task` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../../utils/formatDate` | `formatDateTime` |
| `../../utils/safeUrl` | `safeExternalHref` |
| `../feedback/QueryState` | `QueryErrorState` |
| `../requestSources/RequestSourceLinksPanel` | `RequestSourceLinksPanel` |
| `@tanstack/react-query` | `useInfiniteQuery`, `useMutation`, `useQuery`, `useQueryClient` |
| `clsx` | `clsx` |
| `lucide-react` | `Bot`, `CircleDot`, `GitBranch`, `History`, `Link`, `Plus`, `RefreshCw`, `Trash2`, `X` |
| `react` | `useState`, `KeyboardEvent` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskTimelinePanel` |
| Constants | `t`, `itemLabels`, `githubUrlPattern` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/feedback/QueryState.tsx"]
    n1["frontend/src/components/requestSources/RequestSourceLinksPanel.tsx"]
    n2["frontend/src/components/tasks/TaskForm.tsx"]
    n3["frontend/src/components/tasks/TaskTimelinePanel.test.tsx"]
    n4["frontend/src/components/tasks/TaskTimelinePanel.tsx"]
    n5["frontend/src/i18n/i18n.ts"]
    n6["frontend/src/services/taskService.ts"]
    n7["frontend/src/types/task.ts"]
    n8["frontend/src/utils/apiError.ts"]
    n9["frontend/src/utils/formatDate.ts"]
    n10["frontend/src/utils/safeUrl.ts"]
    n0 --> n8
    n1 --> n0
    n1 --> n5
    n1 --> n8
    n1 --> n10
    n2 --> n0
    n2 --> n4
    n2 --> n6
    n2 --> n7
    n2 --> n8
    n2 --> n9
    n3 --> n4
    n3 --> n7
    n4 --> n0
    n4 --> n1
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n4 --> n9
    n4 --> n10
    n6 --> n7
    click n0 "../modules/QueryState.md"
    click n1 "../modules/RequestSourceLinksPanel.md"
    click n2 "../modules/TaskForm.md"
    click n3 "../modules/TaskTimelinePanel.test.md"
    click n4 "../modules/TaskTimelinePanel.md"
    click n5 "../modules/i18n.md"
    click n6 "../modules/taskService.md"
    click n7 "../modules/types_task.md"
    click n8 "../modules/apiError.md"
    click n9 "../modules/formatDate.md"
    click n10 "../modules/safeUrl.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskForm](../modules/TaskForm.md) |
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
| [TaskTimelinePanelProps](../entities/TaskTimelinePanelProps.md) | Class | 17 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskTimelinePanel` | `({ task }: TaskTimelinePanelProps)` | — | — |