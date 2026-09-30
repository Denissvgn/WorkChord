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
    n1["frontend/src/components/tasks/BacklogPanel.tsx"]
    n2["frontend/src/components/tasks/DraftDismissalDialog.tsx"]
    n3["frontend/src/components/tasks/GuardedTaskModal.tsx"]
    n4["frontend/src/components/tasks/TaskForm.tsx"]
    n5["frontend/src/components/tasks/TaskList.tsx"]
    n6["frontend/src/components/tasks/useDraftDismissal.ts"]
    n7["frontend/src/pages/MyWorkPage.tsx"]
    n8["frontend/src/pages/ProjectDetailPage.tsx"]
    n9["frontend/src/pages/TasksPage.tsx"]
    n1 --> n3
    n2 --> n6
    n3 --> n0
    n3 --> n2
    n3 --> n4
    n3 --> n6
    n5 --> n0
    n5 --> n3
    n7 --> n3
    n8 --> n0
    n8 --> n3
    n9 --> n1
    n9 --> n3
    n9 --> n5
    click n0 "../modules/Modal.md"
    click n1 "../modules/BacklogPanel.md"
    click n2 "../modules/DraftDismissalDialog.md"
    click n3 "../modules/GuardedTaskModal.md"
    click n4 "../modules/TaskForm.md"
    click n5 "../modules/TaskList.md"
    click n6 "../modules/useDraftDismissal.md"
    click n7 "../modules/MyWorkPage.md"
    click n8 "../modules/ProjectDetailPage.md"
    click n9 "../modules/TasksPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [BacklogPanel](../modules/BacklogPanel.md) |
| Inbound | [TaskList](../modules/TaskList.md) |
| Inbound | [MyWorkPage](../modules/MyWorkPage.md) |
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
