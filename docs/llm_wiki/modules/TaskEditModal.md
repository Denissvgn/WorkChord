# TaskEditModal Module

**Path:** `frontend/src/components/gantt/TaskEditModal.tsx`

## Description

_Auto-generated from `frontend/src/components/gantt/TaskEditModal.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/taskService` | `taskService` |
| `../../services/teamService` | `teamService` |
| `../../types/gantt` | `GanttTask` |
| `../../types/task` | `Task`, `TaskUpdate` |
| `../common/Button` | `Button` |
| `../common/ConfirmDialog` | `ConfirmDialog` |
| `../feedback/QueryState` | `QueryErrorState` |
| `../tasks/TaskForm` | `TaskForm` |
| `../ui/SlideOverDrawer` | `SlideOverDrawer` |
| `@tanstack/react-query` | `useQuery` |
| `lucide-react` | `Loader2` |
| `react` | `useMemo`, `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskEditModal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/ConfirmDialog.tsx"]
    n2["frontend/src/components/feedback/QueryState.tsx"]
    n3["frontend/src/components/gantt/GanttChart.tsx"]
    n4["frontend/src/components/gantt/TaskEditModal.tsx"]
    n5["frontend/src/components/tasks/TaskForm.tsx"]
    n6["frontend/src/components/ui/SlideOverDrawer.tsx"]
    n7["frontend/src/pages/GanttPage.tsx"]
    n8["frontend/src/services/taskService.ts"]
    n9["frontend/src/services/teamService.ts"]
    n10["frontend/src/types/gantt.ts"]
    n11["frontend/src/types/task.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n3 --> n2
    n3 --> n4
    n3 --> n10
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n5
    n4 --> n6
    n4 --> n8
    n4 --> n9
    n4 --> n10
    n4 --> n11
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n8
    n5 --> n9
    n5 --> n11
    n7 --> n0
    n7 --> n1
    n7 --> n3
    n7 --> n4
    n7 --> n8
    n7 --> n10
    n7 --> n11
    n8 --> n11
    n10 --> n11
    click n0 "../modules/Button.md"
    click n1 "../modules/ConfirmDialog.md"
    click n2 "../modules/QueryState.md"
    click n3 "../modules/GanttChart.md"
    click n4 "../modules/TaskEditModal.md"
    click n5 "../modules/TaskForm.md"
    click n6 "../modules/SlideOverDrawer.md"
    click n7 "../modules/GanttPage.md"
    click n8 "../modules/taskService.md"
    click n9 "../modules/teamService.md"
    click n10 "../modules/types_gantt.md"
    click n11 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GanttChart](../modules/GanttChart.md) |
| Inbound | [GanttPage](../modules/GanttPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [ConfirmDialog](../modules/ConfirmDialog.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [TaskForm](../modules/TaskForm.md) |
| Outbound | [SlideOverDrawer](../modules/SlideOverDrawer.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [types_gantt](../modules/types_gantt.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskEditModalProps](../entities/TaskEditModalProps.md) | Class | 15 | — | — |
| [TaskEditModalContentProps](../entities/TaskEditModalContentProps.md) | Class | 66 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskEditModal` | `({     task,     iterationId,     isOpen,     onClose,     sandboxMode = false,     onSaveSandbox, }: TaskEditModalProps)` | — | — |
