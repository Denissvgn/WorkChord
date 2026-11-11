# TaskBulkOperationsPanel Module

**Path:** `frontend/src/components/tasks/TaskBulkOperationsPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskBulkOperationsPanel.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/mutationFeedback` | `MutationFeedbackMeta` | Declaration | erased |
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../../services/projectService` | `projectService` | — | compiler-dependent |
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../services/teamService` | `teamService` | — | compiler-dependent |
| `../../types/task` | `Task`, `TaskBulkAction`, `TaskBulkOperationRequest`, `TaskBulkOperationResponse`, `TaskBulkOperationResult`, `TaskStatus` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `lucide-react` | `Bot`, `CheckCircle2`, `ClipboardCheck`, `Trash2`, `XCircle` | — | compiler-dependent |
| `react` | `useEffect`, `useMemo`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskBulkOperationsPanel` |
| Constants | `t`, `ACTION_OPTIONS`, `STATUS_OPTIONS` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/components/tasks/TaskBulkOperationsPanel.tsx"]
    n3["frontend/src/components/tasks/TaskList.tsx"]
    n4["frontend/src/features/mutationFeedback.ts"]
    n5["frontend/src/i18n/i18n.ts"]
    n6["frontend/src/services/iterationService.ts"]
    n7["frontend/src/services/projectService.ts"]
    n8["frontend/src/services/taskService.ts"]
    n9["frontend/src/services/teamService.ts"]
    n10["frontend/src/types/task.ts"]
    n11["frontend/src/utils/apiError.ts"]
    n1 --> n0
    n1 --> n11
    n2 --> n0
    n2 --> n1
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n2 --> n8
    n2 --> n9
    n2 --> n10
    n2 --> n11
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n8
    n3 --> n10
    n3 --> n11
    n7 --> n10
    n8 --> n10
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/TaskBulkOperationsPanel.md"
    click n3 "../modules/TaskList.md"
    click n4 "../modules/mutationFeedback.md"
    click n5 "../modules/i18n.md"
    click n6 "../modules/iterationService.md"
    click n7 "../modules/projectService.md"
    click n8 "../modules/taskService.md"
    click n9 "../modules/teamService.md"
    click n10 "../modules/types_task.md"
    click n11 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskList](../modules/TaskList.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [mutationFeedback](../modules/mutationFeedback.md) |
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
| [TaskBulkOperationsPanelProps](../entities/TaskBulkOperationsPanelProps.md) | Interface | 25 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskBulkOperationsPanel` | <pre><code>&#40;&#123;&#10;    iterationId&#44;&#10;    selectedTasks&#44;&#10;    selectedTaskIds&#44;&#10;    onClearSelection&#44;&#10;    onApplied&#44;&#10;    focusAssignee &#61; false&#44;&#10;&#125;&#58; TaskBulkOperationsPanelProps&#41;</code></pre> | — | — |
