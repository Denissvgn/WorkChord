# TaskEditorDrawer Module

**Path:** `frontend/src/components/tasks/TaskEditorDrawer.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskEditorDrawer.tsx`._

The drawer opens a fresh bounded task detail projection, displays context completeness and keeps draft dismissal explicit. Each opening owns a separate query identity, so a form waits for its current read instead of initializing from a closed editor's cache before garbage collection. Prefix invalidation still refreshes the active editor; authoritative execution uses the complete server context.

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
| `react` | `useId`, `useMemo`, `ReactNode`, `RefObject` |
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
    n0["frontend"]
    n1["frontend/src/components/tasks/TaskEditorDrawer.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/TaskEditorDrawer.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (4) |
| Outbound | `frontend` (8) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [DrawerCopy](../entities/DrawerCopy.md) | Type alias | 16 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskEditorDrawer` | `({     taskId,     iterationId,     open,     onClose,     mode = 'direct',     prepareTask,     onSaveSandbox,     title,     subtitle,     icon,     beforeForm,     className,     restoreFocusRef, }: {     taskId: number \| null;     iterationId?: number;     open: boolean;     onClose: () => void;     mode?: 'direct' \| 'sandbox';     prepareTask?: (task: Task) => Task;     onSaveSandbox?: (update: TaskUpdate) => void;     title?: DrawerCopy;     subtitle?: DrawerCopy;     icon?: ReactNode;     beforeForm?: ReactNode;     className?: string;     restoreFocusRef?: RefObject<HTMLElement \| null>; })` | — | — |