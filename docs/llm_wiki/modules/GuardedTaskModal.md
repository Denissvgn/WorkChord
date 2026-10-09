# GuardedTaskModal Module

**Path:** `frontend/src/components/tasks/GuardedTaskModal.tsx`

## Description

Current task modal openings own a unique, abortable authoritative detail read and wait before constructing a clean form. One coherent snapshot initializes title, version, criteria and acceptance. Background reads preserve active input and its observed version; lower and obsolete responses cannot rebase it. Failed or denied reads withhold server actions, with isolated task draft recovery preserved.

## Imports

| Source | Symbols |
|--------|---------|
| `../../types/task` | `Task` |
| `../common/Modal` | `Modal` |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` |
| `./DraftDismissalDialog` | `DraftDismissalDialog` |
| `./TaskForm` | `TaskForm` |
| `./taskEditorSnapshot` | `readTaskEditorSnapshot`, `keepNewestTaskSnapshot` |
| `./useDraftDismissal` | `useDraftDismissal` |
| `@tanstack/react-query` | `useQuery` |
| `react` | `useId`, `useState`, `ComponentProps`, `ReactNode` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `CurrentTaskModal`, `GuardedTaskModal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/tasks/GuardedTaskModal.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/GuardedTaskModal.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (6) |
| Outbound | `frontend` (7) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

> All 13 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [FormProps](../entities/FormProps.md) | Type alias | 12 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `GuardedTaskModal` | `({ title, closeLabel, onClose, ...form }: FormProps & {     title: ReactNode; closeLabel: string; onClose: () => void; })` | — | — |
| `CurrentTaskModal` | `({ taskId, onClose }: { taskId: number; onClose: () => void })` | — | — |
