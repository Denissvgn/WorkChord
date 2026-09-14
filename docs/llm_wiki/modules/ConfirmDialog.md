# ConfirmDialog Module

**Path:** `frontend/src/components/common/ConfirmDialog.tsx`

## Description

_Auto-generated from `frontend/src/components/common/ConfirmDialog.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `./Button` | `Button` |
| `./Modal` | `Modal` |
| `clsx` | `clsx` |
| `lucide-react` | `AlertTriangle` |
| `react` | `useRef`, `ReactNode` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ConfirmDialog`, `ConfirmDialogProps`, `ConfirmDialogTone` |
| Constants | `toneTitleClassName` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/ConfirmDialog.tsx"]
    n2["frontend/src/components/common/Modal.tsx"]
    n3["frontend/src/components/common/useConfirmDialog.tsx"]
    n4["frontend/src/components/gantt/TaskEditModal.tsx"]
    n5["frontend/src/components/iteration/IterationList.tsx"]
    n6["frontend/src/components/projects/ProjectIterationsSection.tsx"]
    n7["frontend/src/components/tasks/TaskEditorDrawer.tsx"]
    n8["frontend/src/components/tasks/TaskForm.tsx"]
    n9["frontend/src/components/tasks/TaskList.tsx"]
    n10["frontend/src/pages/GanttPage.tsx"]
    n11["frontend/src/pages/ProjectDetailPage.tsx"]
    n1 --> n0
    n1 --> n2
    n3 --> n1
    n4 --> n0
    n4 --> n1
    n4 --> n8
    n5 --> n0
    n5 --> n1
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n7 --> n0
    n7 --> n1
    n7 --> n8
    n8 --> n0
    n8 --> n1
    n9 --> n0
    n9 --> n1
    n9 --> n2
    n9 --> n8
    n10 --> n0
    n10 --> n1
    n10 --> n2
    n10 --> n4
    n11 --> n0
    n11 --> n1
    n11 --> n2
    n11 --> n6
    click n0 "../modules/Button.md"
    click n1 "../modules/ConfirmDialog.md"
    click n2 "../modules/Modal.md"
    click n3 "../modules/useConfirmDialog.md"
    click n4 "../modules/TaskEditModal.md"
    click n5 "../modules/IterationList.md"
    click n6 "../modules/ProjectIterationsSection.md"
    click n7 "../modules/TaskEditorDrawer.md"
    click n8 "../modules/TaskForm.md"
    click n9 "../modules/TaskList.md"
    click n10 "../modules/GanttPage.md"
    click n11 "../modules/ProjectDetailPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [useConfirmDialog](../modules/useConfirmDialog.md) |
| Inbound | [TaskEditModal](../modules/TaskEditModal.md) |
| Inbound | [IterationList](../modules/IterationList.md) |
| Inbound | [ProjectIterationsSection](../modules/ProjectIterationsSection.md) |
| Inbound | [TaskEditorDrawer](../modules/TaskEditorDrawer.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TaskList](../modules/TaskList.md) |
| Inbound | [GanttPage](../modules/GanttPage.md) |
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Modal](../modules/Modal.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ConfirmDialogProps](../entities/ConfirmDialogProps.md) | Class | 10 | — | — |
| [ConfirmDialogTone](../entities/ConfirmDialogTone.md) | Type alias | 8 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ConfirmDialog` | `({     open,     title,     description,     confirmLabel,     cancelLabel,     closeLabel,     onConfirm,     onCancel,     tone = 'danger',     pending = false, }: ConfirmDialogProps)` | — | A deliberately small destructive-action contract layered on the shared |
