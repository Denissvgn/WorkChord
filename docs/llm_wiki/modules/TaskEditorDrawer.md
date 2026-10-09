# TaskEditorDrawer Module

**Path:** `frontend/src/components/tasks/TaskEditorDrawer.tsx`

## Description

Each drawer opening now retains its initial coherent snapshot while the user types. Explicit context reload goes through the established dirty/pending dismissal guard and remounts the form only with the deliberately chosen current version. Snapshot requests are abortable and lower-version responses are ignored.

## Imports

| Source | Symbols |
|--------|---------|
| `../../types/task` | `Task`, `TaskUpdate` |
| `../common/Button` | `Button` |
| `../ui/SlideOverDrawer` | `SlideOverDrawer` |
| `./DraftDismissalDialog` | `DraftDismissalDialog` |
| `./TaskContextSummary` | `TaskContextSummary` |
| `./TaskForm` | `TaskForm` |
| `./taskEditorSnapshot` | `readTaskEditorSnapshot`, `keepNewestTaskSnapshot` |
| `./useDraftDismissal` | `useDraftDismissal` |
| `@tanstack/react-query` | `useQuery` |
| `lucide-react` | `Loader2` |
| `react` | `useId`, `useMemo`, `useState`, `ReactNode`, `RefObject` |
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