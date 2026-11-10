# StatusChangeControl Module

**Path:** `frontend/src/components/tasks/StatusChangeControl.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/StatusChangeControl.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../types/task` | `Task`, `TaskStatus`, `CascadeUpdateInfo` | Declaration | erased |
| `../../utils/formatDate` | `formatDate` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/Modal` | `Modal` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `../ui/tone` | `pillToneClassName`, `STATUS_TONE` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQueryClient` | — | compiler-dependent |
| `lucide-react` | `ArrowRight`, `AlertTriangle`, `Check` | — | compiler-dependent |
| `react` | `useEffect`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `StatusChangeControl` |
| Constants | `VALID_TRANSITIONS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Modal.tsx"]
    n2["frontend/src/components/feedback/QueryState.tsx"]
    n3["frontend/src/components/tasks/StatusChangeControl.tsx"]
    n4["frontend/src/components/tasks/TaskForm.tsx"]
    n5["frontend/src/components/ui/tone.ts"]
    n6["frontend/src/services/taskService.ts"]
    n7["frontend/src/types/task.ts"]
    n8["frontend/src/utils/formatDate.ts"]
    n2 --> n0
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n4 --> n0
    n4 --> n2
    n4 --> n3
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n5 --> n7
    n6 --> n7
    click n0 "../modules/Button.md"
    click n1 "../modules/Modal.md"
    click n2 "../modules/QueryState.md"
    click n3 "../modules/StatusChangeControl.md"
    click n4 "../modules/TaskForm.md"
    click n5 "../modules/tone.md"
    click n6 "../modules/taskService.md"
    click n7 "../modules/types_task.md"
    click n8 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Modal](../modules/Modal.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [tone](../modules/tone.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [formatDate](../modules/formatDate.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [StatusChangeControlProps](../entities/StatusChangeControlProps.md) | Interface | 13 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `StatusChangeControl` | `({ task, iterationId, onStatusChanged, onPendingChange }: StatusChangeControlProps)` | — | — |
