# TaskEditorDrawer Module

**Path:** `frontend/src/components/tasks/TaskEditorDrawer.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskEditorDrawer.tsx`._

The drawer opens a fresh bounded task detail projection, displays context completeness and keeps draft dismissal explicit. Its editor-specific query does not reuse a previous closed editor’s version; authoritative execution still uses the complete server context.

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/taskService` | `taskService` |
| `../../types/task` | `Task`, `TaskUpdate` |
| `../common/Button` | `Button` |
| `../ui/SlideOverDrawer` | `SlideOverDrawer` |
| `./DraftDismissalDialog` | `DraftDismissalDialog` |
| `./TaskContextSummary` | `TaskContextSummary` |
| `./TaskForm` | `TaskForm` |
| `./useDraftDismissal` | `useDraftDismissal` |
| `@tanstack/react-query` | `useQuery` |
| `lucide-react` | `Loader2` |
| `react` | `useMemo`, `ReactNode`, `RefObject` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `useNavigate`, `useSearchParams` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskEditorDrawer` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/projects/ProjectTaskTree.tsx"]
    n2["frontend/src/components/tasks/DraftDismissalDialog.tsx"]
    n3["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n4["frontend/src/components/tasks/TaskContextSummary.tsx"]
    n5["frontend/src/components/tasks/TaskEditorDrawer.tsx"]
    n6["frontend/src/components/tasks/TaskForm.tsx"]
    n7["frontend/src/components/tasks/useDraftDismissal.ts"]
    n8["frontend/src/components/ui/SlideOverDrawer.tsx"]
    n9["frontend/src/pages/TasksPage.tsx"]
    n10["frontend/src/services/taskService.ts"]
    n11["frontend/src/types/task.ts"]
    n1 --> n5
    n1 --> n11
    n2 --> n7
    n3 --> n0
    n3 --> n5
    n3 --> n10
    n3 --> n11
    n4 --> n0
    n4 --> n10
    n4 --> n11
    n5 --> n0
    n5 --> n2
    n5 --> n4
    n5 --> n6
    n5 --> n7
    n5 --> n8
    n5 --> n10
    n5 --> n11
    n6 --> n0
    n6 --> n10
    n6 --> n11
    n9 --> n0
    n9 --> n3
    n9 --> n5
    n9 --> n10
    n10 --> n11
    click n0 "../modules/Button.md"
    click n1 "../modules/ProjectTaskTree.md"
    click n2 "../modules/DraftDismissalDialog.md"
    click n3 "../modules/KanbanBoard.md"
    click n4 "../modules/TaskContextSummary.md"
    click n5 "../modules/TaskEditorDrawer.md"
    click n6 "../modules/TaskForm.md"
    click n7 "../modules/useDraftDismissal.md"
    click n8 "../modules/SlideOverDrawer.md"
    click n9 "../modules/TasksPage.md"
    click n10 "../modules/taskService.md"
    click n11 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ProjectTaskTree](../modules/ProjectTaskTree.md) |
| Inbound | [KanbanBoard](../modules/KanbanBoard.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [DraftDismissalDialog](../modules/DraftDismissalDialog.md) |
| Outbound | [TaskContextSummary](../modules/TaskContextSummary.md) |
| Outbound | [TaskForm](../modules/TaskForm.md) |
| Outbound | [useDraftDismissal](../modules/useDraftDismissal.md) |
| Outbound | [SlideOverDrawer](../modules/SlideOverDrawer.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [DrawerCopy](../entities/DrawerCopy.md) | Type alias | 16 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskEditorDrawer` | `({     taskId,     iterationId,     open,     onClose,     mode = 'direct',     prepareTask,     onSaveSandbox,     title,     subtitle,     icon,     beforeForm,     className,     restoreFocusRef, }: {     taskId: number \| null;     iterationId?: number;     open: boolean;     onClose: () => void;     mode?: 'direct' \| 'sandbox';     prepareTask?: (task: Task) => Task;     onSaveSandbox?: (update: TaskUpdate) => void;     title?: DrawerCopy;     subtitle?: DrawerCopy;     icon?: ReactNode;     beforeForm?: ReactNode;     className?: string;     restoreFocusRef?: RefObject<HTMLElement \| null>; })` | — | — |