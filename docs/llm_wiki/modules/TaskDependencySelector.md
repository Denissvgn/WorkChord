# TaskDependencySelector Module

**Path:** `frontend/src/components/tasks/TaskDependencySelector.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskDependencySelector.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../i18n/i18n` | `i18n` |
| `../../services/taskService` | `taskService` |
| `../../types/task` | `Task` |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` |
| `@tanstack/react-query` | `useQuery` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskDependencySelector` |
| Constants | `t` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/feedback/QueryState.tsx"]
    n1["frontend/src/components/tasks/TaskDependencySelector.tsx"]
    n2["frontend/src/components/tasks/TaskForm.tsx"]
    n3["frontend/src/i18n/i18n.ts"]
    n4["frontend/src/pages/TriagePage.tsx"]
    n5["frontend/src/services/taskService.ts"]
    n6["frontend/src/types/task.ts"]
    n1 --> n0
    n1 --> n3
    n1 --> n5
    n1 --> n6
    n2 --> n0
    n2 --> n1
    n2 --> n5
    n2 --> n6
    n4 --> n0
    n4 --> n1
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n5 --> n6
    click n0 "../modules/QueryState.md"
    click n1 "../modules/TaskDependencySelector.md"
    click n2 "../modules/TaskForm.md"
    click n3 "../modules/i18n.md"
    click n4 "../modules/TriagePage.md"
    click n5 "../modules/taskService.md"
    click n6 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskDependencySelectorProps](../entities/TaskDependencySelectorProps.md) | Class | 9 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskDependencySelector` | `({ iterationId, currentTaskId, selectedIds, onChange }: TaskDependencySelectorProps)` | — | — |
