# TaskWorkPanel Module

**Path:** `frontend/src/components/tasks/TaskWorkPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskWorkPanel.tsx`._

Workflow actions, criterion progress and independent review use explicit server commands. Unsaved evidence gates other commands; metadata editing pauses while a progress/action draft is active. Stale evidence drafts remain visible for review and explicit reapplication. Rejected saves retain their content, and explicit discard clears the progress draft.

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/iterationService` | `iterationService` |
| `../../services/taskService` | `taskService` |
| `../../types/task` | `CriterionProgress`, `Task` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../common/Button` | `Button` |
| `../common/Input` | `Input` |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` |
| `@tanstack/react-query` | `useMutation`, `useQuery` |
| `react` | `useEffect`, `useId`, `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskWorkPanel` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Input.tsx"]
    n2["frontend/src/components/feedback/QueryState.tsx"]
    n3["frontend/src/components/tasks/TaskForm.tsx"]
    n4["frontend/src/components/tasks/TaskWorkPanel.test.tsx"]
    n5["frontend/src/components/tasks/TaskWorkPanel.tsx"]
    n6["frontend/src/services/iterationService.ts"]
    n7["frontend/src/services/taskService.ts"]
    n8["frontend/src/types/task.ts"]
    n9["frontend/src/utils/apiError.ts"]
    n2 --> n0
    n2 --> n9
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n3 --> n9
    n4 --> n5
    n4 --> n8
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n6
    n5 --> n7
    n5 --> n8
    n5 --> n9
    n7 --> n8
    click n0 "../modules/Button.md"
    click n1 "../modules/Input.md"
    click n2 "../modules/QueryState.md"
    click n3 "../modules/TaskForm.md"
    click n4 "../modules/TaskWorkPanel.test.md"
    click n5 "../modules/TaskWorkPanel.md"
    click n6 "../modules/iterationService.md"
    click n7 "../modules/taskService.md"
    click n8 "../modules/types_task.md"
    click n9 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TaskWorkPanel.test](../modules/TaskWorkPanel.test.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Input](../modules/Input.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [iterationService](../modules/iterationService.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskWorkPanel` | `({ task, disabled, draftKey, onDirty, onPending, onUpdated, onReload }: {     task: Task; disabled: boolean; draftKey: string \| null; onDirty: (dirty: boolean) => void;     onPending: (pending: boolean) => void; onUpdated: (task: Task) => void; onReload: () => void; })` | — | — |