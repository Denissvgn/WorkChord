# QuickCapture Module

**Path:** `frontend/src/components/tasks/QuickCapture.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/QuickCapture.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/mutationFeedback` | `MutationFeedbackMeta` | Specifier | compiler-dependent |
| `../../features/mutationFeedback` | `feedbackMessage` | — | compiler-dependent |
| `../../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../services/triageService` | `triageService` | — | compiler-dependent |
| `../../types/task` | `Task` | Declaration | erased |
| `../../types/triage` | `TriageItem` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `CornerDownLeft`, `Plus` | — | compiler-dependent |
| `react` | `FormEvent` | Specifier | compiler-dependent |
| `react` | `useId`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `QuickCapture`, `QuickCaptureTarget` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/tasks/QuickCapture.test.tsx"]
    n2["frontend/src/components/tasks/QuickCapture.tsx"]
    n3["frontend/src/components/triage/TriageList.tsx"]
    n4["frontend/src/features/mutationFeedback.ts"]
    n5["frontend/src/pages/TasksPage.tsx"]
    n6["frontend/src/services/iterationService.ts"]
    n7["frontend/src/services/taskService.ts"]
    n8["frontend/src/services/triageService.ts"]
    n9["frontend/src/types/task.ts"]
    n10["frontend/src/types/triage.ts"]
    n11["frontend/src/utils/apiError.ts"]
    n1 --> n2
    n2 --> n0
    n2 --> n4
    n2 --> n6
    n2 --> n7
    n2 --> n8
    n2 --> n9
    n2 --> n10
    n2 --> n11
    n3 --> n0
    n3 --> n2
    n3 --> n10
    n5 --> n0
    n5 --> n2
    n5 --> n6
    n5 --> n7
    n5 --> n9
    n7 --> n9
    n8 --> n10
    n9 --> n10
    n10 --> n9
    click n0 "../modules/Button.md"
    click n1 "../modules/QuickCapture.test.md"
    click n2 "../modules/QuickCapture.md"
    click n3 "../modules/TriageList.md"
    click n4 "../modules/mutationFeedback.md"
    click n5 "../modules/TasksPage.md"
    click n6 "../modules/iterationService.md"
    click n7 "../modules/taskService.md"
    click n8 "../modules/triageService.md"
    click n9 "../modules/types_task.md"
    click n10 "../modules/types_triage.md"
    click n11 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [QuickCapture.test](../modules/QuickCapture.test.md) |
| Inbound | [TriageList](../modules/TriageList.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [mutationFeedback](../modules/mutationFeedback.md) |
| Outbound | [iterationService](../modules/iterationService.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [triageService](../modules/triageService.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [types_triage](../modules/types_triage.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [QuickCaptureTarget](../entities/QuickCaptureTarget.md) | Type alias | 15 | `{ kind: 'task'; iterationId: number } \| { kind: 'triage' }` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `QuickCapture` | <pre><code>&#40;&#123; target&#44; onExpand&#44; listRow &#61; false &#125;&#58; &#123;&#10;    target&#58; QuickCaptureTarget&#59;&#10;    onExpand&#58; &#40;title&#58; string&#41; &#61;&#62; void&#59;&#10;    listRow&#63;&#58; boolean&#59;&#10;&#125;&#41;</code></pre> | — | One line that captures work from a title and Enter. Priority is left to the |
