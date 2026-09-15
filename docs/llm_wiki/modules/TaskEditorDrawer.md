# TaskEditorDrawer Module

**Path:** `frontend/src/components/tasks/TaskEditorDrawer.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskEditorDrawer.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/taskService` | `taskService` |
| `../../types/task` | `Task`, `TaskUpdate` |
| `../common/Button` | `Button` |
| `../ui/SlideOverDrawer` | `SlideOverDrawer` |
| `./DraftDismissalDialog` | `DraftDismissalDialog` |
| `./TaskForm` | `TaskForm` |
| `./useDraftDismissal` | `useDraftDismissal` |
| `@tanstack/react-query` | `useQuery` |
| `lucide-react` | `Loader2` |
| `react` | `useMemo`, `ReactNode`, `RefObject` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskEditorDrawer` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/tasks/DraftDismissalDialog.tsx"]
    n2["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n3["frontend/src/components/tasks/TaskEditorDrawer.tsx"]
    n4["frontend/src/components/tasks/TaskForm.tsx"]
    n5["frontend/src/components/tasks/useDraftDismissal.ts"]
    n6["frontend/src/components/ui/SlideOverDrawer.tsx"]
    n7["frontend/src/pages/TasksPage.tsx"]
    n8["frontend/src/services/taskService.ts"]
    n9["frontend/src/types/task.ts"]
    n1 --> n5
    n2 --> n0
    n2 --> n3
    n2 --> n8
    n2 --> n9
    n3 --> n0
    n3 --> n1
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n3 --> n8
    n3 --> n9
    n4 --> n0
    n4 --> n8
    n4 --> n9
    n7 --> n0
    n7 --> n2
    n7 --> n3
    n7 --> n8
    n8 --> n9
    click n0 "../modules/Button.md"
    click n1 "../modules/DraftDismissalDialog.md"
    click n2 "../modules/KanbanBoard.md"
    click n3 "../modules/TaskEditorDrawer.md"
    click n4 "../modules/TaskForm.md"
    click n5 "../modules/useDraftDismissal.md"
    click n6 "../modules/SlideOverDrawer.md"
    click n7 "../modules/TasksPage.md"
    click n8 "../modules/taskService.md"
    click n9 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [KanbanBoard](../modules/KanbanBoard.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [DraftDismissalDialog](../modules/DraftDismissalDialog.md) |
| Outbound | [TaskForm](../modules/TaskForm.md) |
| Outbound | [useDraftDismissal](../modules/useDraftDismissal.md) |
| Outbound | [SlideOverDrawer](../modules/SlideOverDrawer.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [DrawerCopy](../entities/DrawerCopy.md) | Type alias | 14 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskEditorDrawer` | `({     taskId,     iterationId,     open,     onClose,     mode = 'direct',     prepareTask,     onSaveSandbox,     title,     subtitle,     icon,     beforeForm,     className,     restoreFocusRef, }: {     taskId: number \| null;     iterationId?: number;     open: boolean;     onClose: () => void;     mode?: 'direct' \| 'sandbox';     prepareTask?: (task: Task) => Task;     onSaveSandbox?: (update: TaskUpdate) => void;     title?: DrawerCopy;     subtitle?: DrawerCopy;     icon?: ReactNode;     beforeForm?: ReactNode;     className?: string;     restoreFocusRef?: RefObject<HTMLElement \| null>; })` | — | — |
