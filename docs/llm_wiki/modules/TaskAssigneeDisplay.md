# TaskAssigneeDisplay Module

**Path:** `frontend/src/components/tasks/TaskAssigneeDisplay.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskAssigneeDisplay.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/agentDispatch` | `AGENT_DISPATCH_LABEL_KEY` | — | compiler-dependent |
| `../../types/gantt` | `GanttTask` | Declaration | erased |
| `../../types/task` | `Task` | Declaration | erased |
| `./useTaskAssigneeDisplay` | `useTaskAssigneeDisplay` | — | compiler-dependent |
| `lucide-react` | `Bot`, `User` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskAssigneeDisplay` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/gantt/GanttChart.tsx"]
    n1["frontend/src/components/tasks/KanbanBoard/KanbanCard.tsx"]
    n2["frontend/src/components/tasks/PipelineView.tsx"]
    n3["frontend/src/components/tasks/TaskAssigneeDisplay.tsx"]
    n4["frontend/src/components/tasks/TaskReadView.tsx"]
    n5["frontend/src/components/tasks/useTaskAssigneeDisplay.ts"]
    n6["frontend/src/features/agentDispatch.ts"]
    n7["frontend/src/types/gantt.ts"]
    n8["frontend/src/types/task.ts"]
    n0 --> n3
    n0 --> n7
    n1 --> n3
    n1 --> n8
    n2 --> n3
    n2 --> n8
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n4 --> n3
    n4 --> n5
    n4 --> n8
    n5 --> n7
    n5 --> n8
    n6 --> n8
    n7 --> n8
    click n0 "../modules/GanttChart.md"
    click n1 "../modules/KanbanCard.md"
    click n2 "../modules/PipelineView.md"
    click n3 "../modules/TaskAssigneeDisplay.md"
    click n4 "../modules/TaskReadView.md"
    click n5 "../modules/useTaskAssigneeDisplay.md"
    click n6 "../modules/agentDispatch.md"
    click n7 "../modules/types_gantt.md"
    click n8 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GanttChart](../modules/GanttChart.md) |
| Inbound | [KanbanCard](../modules/KanbanCard.md) |
| Inbound | [PipelineView](../modules/PipelineView.md) |
| Inbound | [TaskReadView](../modules/TaskReadView.md) |
| Outbound | [useTaskAssigneeDisplay](../modules/useTaskAssigneeDisplay.md) |
| Outbound | [agentDispatch](../modules/agentDispatch.md) |
| Outbound | [types_gantt](../modules/types_gantt.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskAssigneeDisplay` | `({ task, iterationId, bar = false, durationDays }: { task: Task \| GanttTask; iterationId: number \| null; bar?: boolean; durationDays?: number })` | — | The same capacity identity and dispatch line used by the task row, with its Reviewer beside it. |
