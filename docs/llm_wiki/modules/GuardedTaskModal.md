# GuardedTaskModal Module

**Path:** `frontend/src/components/tasks/GuardedTaskModal.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/GuardedTaskModal.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../common/Modal` | `Modal` |
| `./DraftDismissalDialog` | `DraftDismissalDialog` |
| `./TaskForm` | `TaskForm` |
| `./useDraftDismissal` | `useDraftDismissal` |
| `react` | `ComponentProps`, `ReactNode` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `GuardedTaskModal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Modal.tsx"]
    n1["frontend/src/components/tasks/DraftDismissalDialog.tsx"]
    n2["frontend/src/components/tasks/GuardedTaskModal.tsx"]
    n3["frontend/src/components/tasks/TaskForm.tsx"]
    n4["frontend/src/components/tasks/TaskList.tsx"]
    n5["frontend/src/components/tasks/useDraftDismissal.ts"]
    n6["frontend/src/pages/ProjectDetailPage.tsx"]
    n7["frontend/src/pages/TasksPage.tsx"]
    n1 --> n5
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n5
    n4 --> n0
    n4 --> n2
    n6 --> n0
    n6 --> n2
    n7 --> n2
    n7 --> n4
    click n0 "../modules/Modal.md"
    click n1 "../modules/DraftDismissalDialog.md"
    click n2 "../modules/GuardedTaskModal.md"
    click n3 "../modules/TaskForm.md"
    click n4 "../modules/TaskList.md"
    click n5 "../modules/useDraftDismissal.md"
    click n6 "../modules/ProjectDetailPage.md"
    click n7 "../modules/TasksPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskList](../modules/TaskList.md) |
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [Modal](../modules/Modal.md) |
| Outbound | [DraftDismissalDialog](../modules/DraftDismissalDialog.md) |
| Outbound | [TaskForm](../modules/TaskForm.md) |
| Outbound | [useDraftDismissal](../modules/useDraftDismissal.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [FormProps](../entities/FormProps.md) | Type alias | 7 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `GuardedTaskModal` | `({ title, closeLabel, onClose, ...form }: FormProps & {     title: ReactNode; closeLabel: string; onClose: () => void; })` | — | — |
