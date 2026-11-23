# useTaskAssigneeDisplay Module

**Path:** `frontend/src/components/tasks/useTaskAssigneeDisplay.ts`

## Description

_Auto-generated from `frontend/src/components/tasks/useTaskAssigneeDisplay.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../services/teamService` | `teamService` | — | compiler-dependent |
| `../../types/gantt` | `GanttTask` | Declaration | erased |
| `../../types/task` | `Task` | Declaration | erased |
| `./useAgentRowFacts` | `agentRowValues`, `assigneeKind`, `useAgentRowFacts` | — | compiler-dependent |
| `./useTaskRowEdits` | `assigneeOptionsFrom` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `useTaskAssigneeDisplay` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/TaskAssigneeDisplay.tsx"]
    n1["frontend/src/components/tasks/TaskReadView.tsx"]
    n2["frontend/src/components/tasks/useAgentRowFacts.ts"]
    n3["frontend/src/components/tasks/useTaskAssigneeDisplay.ts"]
    n4["frontend/src/components/tasks/useTaskRowEdits.ts"]
    n5["frontend/src/services/taskService.ts"]
    n6["frontend/src/services/teamService.ts"]
    n7["frontend/src/types/gantt.ts"]
    n8["frontend/src/types/task.ts"]
    n0 --> n3
    n0 --> n7
    n0 --> n8
    n1 --> n0
    n1 --> n3
    n1 --> n5
    n1 --> n8
    n2 --> n5
    n2 --> n8
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n4 --> n5
    n4 --> n6
    n4 --> n8
    n5 --> n8
    n7 --> n8
    click n0 "../modules/TaskAssigneeDisplay.md"
    click n1 "../modules/TaskReadView.md"
    click n2 "../modules/useAgentRowFacts.md"
    click n3 "../modules/useTaskAssigneeDisplay.md"
    click n4 "../modules/useTaskRowEdits.md"
    click n5 "../modules/taskService.md"
    click n6 "../modules/teamService.md"
    click n7 "../modules/types_gantt.md"
    click n8 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskAssigneeDisplay](../modules/TaskAssigneeDisplay.md) |
| Inbound | [TaskReadView](../modules/TaskReadView.md) |
| Outbound | [useAgentRowFacts](../modules/useAgentRowFacts.md) |
| Outbound | [useTaskRowEdits](../modules/useTaskRowEdits.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [types_gantt](../modules/types_gantt.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useTaskAssigneeDisplay` | `(task: Task \| GanttTask, iterationId: number \| null)` | — | — |
