# TaskBriefEditor Module

**Path:** `frontend/src/components/tasks/TaskBriefEditor.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskBriefEditor.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../types/task` | `TaskBrief` |
| `../common/Button` | `Button` |
| `./taskEditorContract` | `newCriterion` |
| `lucide-react` | `ArrowDown`, `ArrowUp`, `Plus`, `Trash2` |
| `react` | `useId` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskBriefEditor` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/tasks/TaskBriefEditor.test.tsx"]
    n2["frontend/src/components/tasks/TaskBriefEditor.tsx"]
    n3["frontend/src/components/tasks/taskEditorContract.ts"]
    n4["frontend/src/components/tasks/TaskForm.tsx"]
    n5["frontend/src/pages/TriagePage.tsx"]
    n6["frontend/src/types/task.ts"]
    n1 --> n2
    n1 --> n3
    n2 --> n0
    n2 --> n3
    n2 --> n6
    n3 --> n6
    n4 --> n0
    n4 --> n2
    n4 --> n3
    n4 --> n6
    n5 --> n0
    n5 --> n2
    n5 --> n3
    n5 --> n6
    click n0 "../modules/Button.md"
    click n1 "../modules/TaskBriefEditor.test.md"
    click n2 "../modules/TaskBriefEditor.md"
    click n3 "../modules/taskEditorContract.md"
    click n4 "../modules/TaskForm.md"
    click n5 "../modules/TriagePage.md"
    click n6 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskBriefEditor.test](../modules/TaskBriefEditor.test.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [taskEditorContract](../modules/taskEditorContract.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskBriefEditor` | `({ value, onChange, disabled = false, hideContext = false }: {     value: TaskBrief; onChange: (value: TaskBrief) => void; disabled?: boolean; hideContext?: boolean; })` | — | — |
