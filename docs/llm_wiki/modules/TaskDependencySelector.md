# TaskDependencySelector Module

**Path:** `frontend/src/components/tasks/TaskDependencySelector.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskDependencySelector.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../i18n/i18n` | `i18n` |
| `../../services/taskService` | `taskService` |
| `../common/Button` | `Button` |
| `../common/Input` | `Input` |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` |
| `@tanstack/react-query` | `useQuery` |
| `react` | `useState` |

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
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Input.tsx"]
    n2["frontend/src/components/feedback/QueryState.tsx"]
    n3["frontend/src/components/tasks/TaskDependencySelector.tsx"]
    n4["frontend/src/components/tasks/TaskForm.tsx"]
    n5["frontend/src/i18n/i18n.ts"]
    n6["frontend/src/pages/TriagePage.tsx"]
    n7["frontend/src/services/taskService.ts"]
    n2 --> n0
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n5
    n3 --> n7
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n7
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n5
    n6 --> n7
    click n0 "../modules/Button.md"
    click n1 "../modules/Input.md"
    click n2 "../modules/QueryState.md"
    click n3 "../modules/TaskDependencySelector.md"
    click n4 "../modules/TaskForm.md"
    click n5 "../modules/i18n.md"
    click n6 "../modules/TriagePage.md"
    click n7 "../modules/taskService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Input](../modules/Input.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [taskService](../modules/taskService.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskDependencySelectorProps](../entities/TaskDependencySelectorProps.md) | Class | 11 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskDependencySelector` | `({ iterationId, projectId, currentTaskId, selectedIds, onChange }: TaskDependencySelectorProps)` | — | — |
