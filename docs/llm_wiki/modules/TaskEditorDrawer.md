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
| `../common/ConfirmDialog` | `ConfirmDialog` |
| `../ui/SlideOverDrawer` | `SlideOverDrawer` |
| `./TaskForm` | `TaskForm` |
| `@tanstack/react-query` | `useQuery` |
| `lucide-react` | `Loader2` |
| `react` | `useMemo`, `useState`, `ReactNode`, `RefObject` |
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
    n1["frontend/src/components/common/ConfirmDialog.tsx"]
    n2["frontend/src/components/tasks/TaskEditorDrawer.tsx"]
    n3["frontend/src/components/tasks/TaskForm.tsx"]
    n4["frontend/src/components/ui/SlideOverDrawer.tsx"]
    n5["frontend/src/pages/TasksPage.tsx"]
    n6["frontend/src/services/taskService.ts"]
    n7["frontend/src/types/task.ts"]
    n1 --> n0
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n6
    n2 --> n7
    n3 --> n0
    n3 --> n1
    n3 --> n6
    n3 --> n7
    n5 --> n0
    n5 --> n2
    n5 --> n3
    n5 --> n6
    n6 --> n7
    click n0 "../modules/Button.md"
    click n1 "../modules/ConfirmDialog.md"
    click n2 "../modules/TaskEditorDrawer.md"
    click n3 "../modules/TaskForm.md"
    click n4 "../modules/SlideOverDrawer.md"
    click n5 "../modules/TasksPage.md"
    click n6 "../modules/taskService.md"
    click n7 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [ConfirmDialog](../modules/ConfirmDialog.md) |
| Outbound | [TaskForm](../modules/TaskForm.md) |
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
| [DrawerCopy](../entities/DrawerCopy.md) | Type alias | 13 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskEditorDrawer` | `({     taskId,     iterationId,     open,     onClose,     mode = 'direct',     prepareTask,     onSaveSandbox,     title,     subtitle,     icon,     beforeForm,     className,     restoreFocusRef, }: {     taskId: number \| null;     iterationId?: number;     open: boolean;     onClose: () => void;     mode?: 'direct' \| 'sandbox';     prepareTask?: (task: Task) => Task;     onSaveSandbox?: (update: TaskUpdate) => void;     title?: DrawerCopy;     subtitle?: DrawerCopy;     icon?: ReactNode;     beforeForm?: ReactNode;     className?: string;     restoreFocusRef?: RefObject<HTMLElement \| null>; })` | — | — |
