# TaskPostponementPanel Module

**Path:** `frontend/src/components/tasks/TaskPostponementPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskPostponementPanel.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/identity/identityContext` | `useIdentity` | — | compiler-dependent |
| `../../features/mutationFeedback` | `MutationFeedbackMeta` | Declaration | erased |
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../types/task` | `ReactivationRequirement`, `Task` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../../utils/formatDate` | `formatDate` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/Textarea` | `Textarea` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `./useDraftDismissal` | `useActiveMount` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `i18next` | `TFunction` | Declaration | erased |
| `react` | `useId`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskPostponementPanel` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Textarea.tsx"]
    n2["frontend/src/components/feedback/QueryState.tsx"]
    n3["frontend/src/components/tasks/TaskPostponementPanel.tsx"]
    n4["frontend/src/components/tasks/TaskWorkPanel.tsx"]
    n5["frontend/src/components/tasks/useDraftDismissal.ts"]
    n6["frontend/src/features/identity/identityContext.ts"]
    n7["frontend/src/features/mutationFeedback.ts"]
    n8["frontend/src/services/taskService.ts"]
    n9["frontend/src/types/task.ts"]
    n10["frontend/src/utils/apiError.ts"]
    n11["frontend/src/utils/formatDate.ts"]
    n2 --> n0
    n2 --> n10
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n3 --> n9
    n3 --> n10
    n3 --> n11
    n4 --> n0
    n4 --> n2
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n4 --> n9
    n4 --> n10
    n8 --> n9
    n10 --> n9
    click n0 "../modules/Button.md"
    click n1 "../modules/Textarea.md"
    click n2 "../modules/QueryState.md"
    click n3 "../modules/TaskPostponementPanel.md"
    click n4 "../modules/TaskWorkPanel.md"
    click n5 "../modules/useDraftDismissal.md"
    click n6 "../modules/identityContext.md"
    click n7 "../modules/mutationFeedback.md"
    click n8 "../modules/taskService.md"
    click n9 "../modules/types_task.md"
    click n10 "../modules/apiError.md"
    click n11 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskWorkPanel](../modules/TaskWorkPanel.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Textarea](../modules/Textarea.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [useDraftDismissal](../modules/useDraftDismissal.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [mutationFeedback](../modules/mutationFeedback.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [apiError](../modules/apiError.md) |
| Outbound | [formatDate](../modules/formatDate.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskPostponementPanel` | <pre><code>&#40;&#123; task&#44; canReactivate&#44; disabled&#44; disabledReasons &#61; &#91;&#93;&#44; onPending&#44; onUpdated &#125;&#58; &#123;&#10;    task&#58; Task&#59; canReactivate&#58; boolean&#59; disabled&#58; boolean&#59; disabledReasons&#63;&#58; string&#91;&#93;&#59; onPending&#58; &#40;pending&#58; boolean&#41; &#61;&#62; void&#59; onUpdated&#58; &#40;task&#58; Task&#41; &#61;&#62; void&#59;&#10;&#125;&#41;</code></pre> | — | What a postponed task is waiting for: the reason, each requirement as met or not met, a place for the |
