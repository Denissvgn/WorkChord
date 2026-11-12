# TaskEditModal Module

**Path:** `frontend/src/components/gantt/TaskEditModal.tsx`

## Description

_Auto-generated from `frontend/src/components/gantt/TaskEditModal.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/teamService` | `teamService` | — | compiler-dependent |
| `../../types/gantt` | `GanttTask` | Declaration | erased |
| `../../types/task` | `Task`, `TaskUpdate` | Declaration | erased |
| `../tasks/TaskEditorDrawer` | `TaskEditorDrawer` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react` | `useCallback` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskEditModal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/gantt/GanttChart.tsx"]
    n1["frontend/src/components/gantt/TaskEditModal.test.tsx"]
    n2["frontend/src/components/gantt/TaskEditModal.tsx"]
    n3["frontend/src/components/tasks/TaskEditorDrawer.tsx"]
    n4["frontend/src/pages/GanttPage.tsx"]
    n5["frontend/src/services/teamService.ts"]
    n6["frontend/src/types/gantt.ts"]
    n7["frontend/src/types/task.ts"]
    n0 --> n2
    n0 --> n6
    n1 --> n2
    n1 --> n6
    n1 --> n7
    n2 --> n3
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n3 --> n7
    n4 --> n0
    n4 --> n2
    n4 --> n6
    n4 --> n7
    n6 --> n7
    click n0 "../modules/GanttChart.md"
    click n1 "../modules/TaskEditModal.test.md"
    click n2 "../modules/TaskEditModal.md"
    click n3 "../modules/TaskEditorDrawer.md"
    click n4 "../modules/GanttPage.md"
    click n5 "../modules/teamService.md"
    click n6 "../modules/types_gantt.md"
    click n7 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GanttChart](../modules/GanttChart.md) |
| Inbound | [TaskEditModal.test](../modules/TaskEditModal.test.md) |
| Inbound | [GanttPage](../modules/GanttPage.md) |
| Outbound | [TaskEditorDrawer](../modules/TaskEditorDrawer.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [types_gantt](../modules/types_gantt.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskEditModalProps](../entities/TaskEditModalProps.md) | Interface | 8 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskEditModal` | <pre><code>&#40;&#123;&#10;    task&#44;&#10;    iterationId&#44;&#10;    isOpen&#44;&#10;    onClose&#44;&#10;    sandboxMode &#61; false&#44;&#10;    onSaveSandbox&#44;&#10;&#125;&#58; TaskEditModalProps&#41;</code></pre> | — | Opens a Gantt task in the same task drawer as the other views: read first, with |
