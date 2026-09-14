# TaskBulkOperationsPanel Module

**Path:** `frontend/src/components/tasks/TaskBulkOperationsPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskBulkOperationsPanel.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../i18n/i18n` | `i18n` |
| `../../services/iterationService` | `iterationService` |
| `../../services/projectService` | `projectService` |
| `../../services/taskService` | `taskService` |
| `../../services/teamService` | `teamService` |
| `../../types/task` | `Task`, `TaskBulkAction`, `TaskBulkOperationRequest`, `TaskBulkOperationResponse`, `TaskBulkOperationResult`, `TaskStatus` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../common/Button` | `Button` |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` |
| `lucide-react` | `Bot`, `CheckCircle2`, `ClipboardCheck`, `Trash2`, `XCircle` |
| `react` | `useMemo`, `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskBulkOperationsPanel` |
| Constants | `t`, `ACTION_OPTIONS`, `STATUS_OPTIONS` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/components/tasks/TaskBulkOperationsPanel.tsx"]
    n3["frontend/src/components/tasks/TaskList.tsx"]
    n4["frontend/src/i18n/i18n.ts"]
    n5["frontend/src/services/iterationService.ts"]
    n6["frontend/src/services/projectService.ts"]
    n7["frontend/src/services/taskService.ts"]
    n8["frontend/src/services/teamService.ts"]
    n9["frontend/src/types/task.ts"]
    n10["frontend/src/utils/apiError.ts"]
    n1 --> n0
    n1 --> n10
    n2 --> n0
    n2 --> n1
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n2 --> n8
    n2 --> n9
    n2 --> n10
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n7
    n3 --> n9
    n3 --> n10
    n6 --> n9
    n7 --> n9
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/TaskBulkOperationsPanel.md"
    click n3 "../modules/TaskList.md"
    click n4 "../modules/i18n.md"
    click n5 "../modules/iterationService.md"
    click n6 "../modules/projectService.md"
    click n7 "../modules/taskService.md"
    click n8 "../modules/teamService.md"
    click n9 "../modules/types_task.md"
    click n10 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskList](../modules/TaskList.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [iterationService](../modules/iterationService.md) |
| Outbound | [projectService](../modules/projectService.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskBulkOperationsPanelProps](../entities/TaskBulkOperationsPanelProps.md) | Class | 24 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskBulkOperationsPanel` | `({     iterationId,     selectedTasks,     selectedTaskIds,     onClearSelection,     onApplied, }: TaskBulkOperationsPanelProps)` | — | — |
