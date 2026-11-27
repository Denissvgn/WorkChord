# ImportTasksModal Module

**Path:** `frontend/src/components/tasks/ImportTasksModal.tsx`

## Description

Text imports capture an observed planning revision before input is enabled. Conflicts retain input and require explicit context reload. File readers are owned by a generation, canceled on replacement/unmount, and prevent submission while pending; stale callbacks cannot replace a later file.

_Auto-generated from `frontend/src/components/tasks/ImportTasksModal.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/mutationFeedback` | `MutationFeedbackMeta` | Declaration | erased |
| `../../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../types/task` | `TaskImportDestination` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage`, `normalizeApiError` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/Modal` | `Modal` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `Upload`, `FileText`, `AlertCircle`, `CheckCircle`, `Maximize2`, `Minimize2`, `Inbox` | — | compiler-dependent |
| `react` | `useEffect`, `useState`, `useRef` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ImportTasksModal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Modal.tsx"]
    n2["frontend/src/components/feedback/QueryState.tsx"]
    n3["frontend/src/components/planning/PlanWorkSection.tsx"]
    n4["frontend/src/components/tasks/ImportTasksModal.tsx"]
    n5["frontend/src/components/tasks/TaskTextEditorModal.test.tsx"]
    n6["frontend/src/features/mutationFeedback.ts"]
    n7["frontend/src/pages/TasksPage.tsx"]
    n8["frontend/src/services/iterationService.ts"]
    n9["frontend/src/services/taskService.ts"]
    n10["frontend/src/types/task.ts"]
    n11["frontend/src/utils/apiError.ts"]
    n2 --> n0
    n2 --> n11
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    n3 --> n8
    n3 --> n9
    n3 --> n10
    n3 --> n11
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n6
    n4 --> n8
    n4 --> n9
    n4 --> n10
    n4 --> n11
    n5 --> n4
    n7 --> n0
    n7 --> n2
    n7 --> n4
    n7 --> n8
    n7 --> n9
    n7 --> n10
    n9 --> n10
    n11 --> n10
    click n0 "../modules/Button.md"
    click n1 "../modules/Modal.md"
    click n2 "../modules/QueryState.md"
    click n3 "../modules/PlanWorkSection.md"
    click n4 "../modules/ImportTasksModal.md"
    click n5 "../modules/TaskTextEditorModal.test.md"
    click n6 "../modules/mutationFeedback.md"
    click n7 "../modules/TasksPage.md"
    click n8 "../modules/iterationService.md"
    click n9 "../modules/taskService.md"
    click n10 "../modules/types_task.md"
    click n11 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PlanWorkSection](../modules/PlanWorkSection.md) |
| Inbound | [TaskTextEditorModal.test](../modules/TaskTextEditorModal.test.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Modal](../modules/Modal.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [mutationFeedback](../modules/mutationFeedback.md) |
| Outbound | [iterationService](../modules/iterationService.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ImportTasksModalProps](../entities/ImportTasksModalProps.md) | Interface | 15 | — | — |
| [ImportTasksBodyProps](../entities/ImportTasksBodyProps.md) | Interface | 29 | `ImportTasksModalProps` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ImportTasksModal` | `({ iterationId, onClose }: ImportTasksModalProps)` | — | — |
