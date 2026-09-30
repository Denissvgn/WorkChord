# DeliveryDependencies Module

**Path:** `frontend/src/components/tasks/DeliveryDependencies.tsx`

## Description

Displays delivery readiness and adds or removes typed prerequisites using the dependent task version. Task search and milestone choices are scoped; unavailable targets remain generic. Failed mutations preserve the current selection and expose reconciliation feedback.

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/api` | `api` |
| `../../services/projectService` | `projectService` |
| `../../services/taskService` | `taskService` |
| `../../types/task` | `Task` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../common/Button` | `Button` |
| `../feedback/QueryState` | `QueryErrorState` |
| `@tanstack/react-query` | `useMutation`, `useQuery` |
| `react` | `useEffect`, `useId`, `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `DeliveryDependencies` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/components/tasks/DeliveryDependencies.tsx"]
    n3["frontend/src/components/tasks/TaskForm.tsx"]
    n4["frontend/src/services/api.ts"]
    n5["frontend/src/services/projectService.ts"]
    n6["frontend/src/services/taskService.ts"]
    n7["frontend/src/types/task.ts"]
    n8["frontend/src/utils/apiError.ts"]
    n1 --> n0
    n1 --> n8
    n2 --> n0
    n2 --> n1
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n2 --> n8
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n5 --> n4
    n5 --> n7
    n6 --> n4
    n6 --> n7
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/DeliveryDependencies.md"
    click n3 "../modules/TaskForm.md"
    click n4 "../modules/api.md"
    click n5 "../modules/projectService.md"
    click n6 "../modules/taskService.md"
    click n7 "../modules/types_task.md"
    click n8 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [projectService](../modules/projectService.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [Dependency](../entities/Dependency.md) | Class | 12 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `DeliveryDependencies` | `({ task, disabled, onPending, onUpdated }: { task: Task; disabled: boolean; onPending: (pending: boolean) => void; onUpdated: (task: Task) => void })` | — | — |
