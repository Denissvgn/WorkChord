# ImportTasksModal Module

**Path:** `frontend/src/components/tasks/ImportTasksModal.tsx`

## Description

Text imports capture an observed planning revision before input is enabled. Conflicts retain input and require explicit context reload. File readers are owned by a generation, canceled on replacement/unmount, and prevent submission while pending; stale callbacks cannot replace a later file.

_Auto-generated from `frontend/src/components/tasks/ImportTasksModal.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/iterationService` | `iterationService` |
| `../../services/taskService` | `taskService` |
| `../../types/task` | `TaskImportDestination` |
| `../../utils/apiError` | `getApiErrorMessage`, `normalizeApiError` |
| `../common/Button` | `Button` |
| `../common/Modal` | `Modal` |
| `../feedback/QueryState` | `QueryErrorState` |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` |
| `clsx` | `clsx` |
| `lucide-react` | `Upload`, `FileText`, `AlertCircle`, `CheckCircle`, `Maximize2`, `Minimize2`, `Inbox` |
| `react` | `useEffect`, `useState`, `useRef` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ImportTasksModal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Modal.tsx"]
    n2["frontend/src/components/feedback/QueryState.tsx"]
    n3["frontend/src/components/tasks/ImportTasksModal.tsx"]
    n4["frontend/src/components/tasks/TaskTextEditorModal.test.tsx"]
    n5["frontend/src/pages/TasksPage.tsx"]
    n6["frontend/src/services/iterationService.ts"]
    n7["frontend/src/services/taskService.ts"]
    n8["frontend/src/types/task.ts"]
    n9["frontend/src/utils/apiError.ts"]
    n2 --> n0
    n2 --> n9
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n3 --> n9
    n4 --> n3
    n5 --> n0
    n5 --> n2
    n5 --> n3
    n5 --> n6
    n5 --> n7
    n7 --> n8
    click n0 "../modules/Button.md"
    click n1 "../modules/Modal.md"
    click n2 "../modules/QueryState.md"
    click n3 "../modules/ImportTasksModal.md"
    click n4 "../modules/TaskTextEditorModal.test.md"
    click n5 "../modules/TasksPage.md"
    click n6 "../modules/iterationService.md"
    click n7 "../modules/taskService.md"
    click n8 "../modules/types_task.md"
    click n9 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskTextEditorModal.test](../modules/TaskTextEditorModal.test.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Modal](../modules/Modal.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
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
| [ImportTasksModalProps](../entities/ImportTasksModalProps.md) | Class | 14 | — | — |
| [ImportTasksBodyProps](../entities/ImportTasksBodyProps.md) | Class | 28 | `ImportTasksModalProps` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ImportTasksModal` | `({ iterationId, onClose }: ImportTasksModalProps)` | — | — |
