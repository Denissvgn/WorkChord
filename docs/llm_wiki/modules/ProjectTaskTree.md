# ProjectTaskTree Module

**Path:** `frontend/src/components/projects/ProjectTaskTree.tsx`

## Description

_Auto-generated from `frontend/src/components/projects/ProjectTaskTree.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../i18n/i18n` | `i18n` |
| `../../types/task` | `Task` |
| `../../utils/formatDate` | `formatDate` |
| `../tasks/TaskEditorDrawer` | `TaskEditorDrawer` |
| `../ui/tone` | `pillToneClassName`, `STATUS_TONE`, `statusTextClassName` |
| `clsx` | `clsx` |
| `lucide-react` | `AlertTriangle`, `CheckCircle2`, `Circle`, `CornerDownRight`, `MessageSquare`, `User` |
| `react` | `useState` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ProjectTaskTree` |
| Constants | `t` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/projects/ProjectTaskTree.tsx"]
    n1["frontend/src/components/tasks/TaskEditorDrawer.tsx"]
    n2["frontend/src/components/ui/tone.ts"]
    n3["frontend/src/i18n/i18n.ts"]
    n4["frontend/src/pages/ProjectDetailPage.tsx"]
    n5["frontend/src/types/task.ts"]
    n6["frontend/src/utils/formatDate.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n5
    n0 --> n6
    n1 --> n5
    n2 --> n5
    n4 --> n0
    n4 --> n2
    n4 --> n3
    n4 --> n6
    click n0 "../modules/ProjectTaskTree.md"
    click n1 "../modules/TaskEditorDrawer.md"
    click n2 "../modules/tone.md"
    click n3 "../modules/i18n.md"
    click n4 "../modules/ProjectDetailPage.md"
    click n5 "../modules/types_task.md"
    click n6 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Outbound | [TaskEditorDrawer](../modules/TaskEditorDrawer.md) |
| Outbound | [tone](../modules/tone.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [formatDate](../modules/formatDate.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ProjectTaskTreeProps](../entities/ProjectTaskTreeProps.md) | Class | 19 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ProjectTaskTree` | `({ tasks }: ProjectTaskTreeProps)` | — | — |
