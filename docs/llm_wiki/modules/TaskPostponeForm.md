# TaskPostponeForm Module

**Path:** `frontend/src/components/tasks/TaskPostponeForm.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskPostponeForm.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/mutationFeedback` | `MutationFeedbackMeta` | Declaration | erased |
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../types/task` | `ReactivationRequirementInput`, `ReactivationRequirementKind`, `Task`, `TaskActions` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/Select` | `Select` | — | compiler-dependent |
| `../common/Textarea` | `Textarea` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `./useDraftDismissal` | `useActiveMount` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery` | — | compiler-dependent |
| `react` | `useEffect`, `useId`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskPostponeForm` |
| Constants | `MAX_REQUIREMENTS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Select.tsx"]
    n2["frontend/src/components/common/Textarea.tsx"]
    n3["frontend/src/components/feedback/QueryState.tsx"]
    n4["frontend/src/components/tasks/TaskPostponeForm.tsx"]
    n5["frontend/src/components/tasks/TaskWorkPanel.tsx"]
    n6["frontend/src/components/tasks/useDraftDismissal.ts"]
    n7["frontend/src/features/mutationFeedback.ts"]
    n8["frontend/src/services/taskService.ts"]
    n9["frontend/src/types/task.ts"]
    n10["frontend/src/utils/apiError.ts"]
    n3 --> n0
    n3 --> n10
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n4 --> n9
    n4 --> n10
    n5 --> n0
    n5 --> n1
    n5 --> n3
    n5 --> n4
    n5 --> n6
    n5 --> n7
    n5 --> n8
    n5 --> n9
    n5 --> n10
    n8 --> n9
    click n0 "../modules/Button.md"
    click n1 "../modules/Select.md"
    click n2 "../modules/Textarea.md"
    click n3 "../modules/QueryState.md"
    click n4 "../modules/TaskPostponeForm.md"
    click n5 "../modules/TaskWorkPanel.md"
    click n6 "../modules/useDraftDismissal.md"
    click n7 "../modules/mutationFeedback.md"
    click n8 "../modules/taskService.md"
    click n9 "../modules/types_task.md"
    click n10 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskWorkPanel](../modules/TaskWorkPanel.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Select](../modules/Select.md) |
| Outbound | [Textarea](../modules/Textarea.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [useDraftDismissal](../modules/useDraftDismissal.md) |
| Outbound | [mutationFeedback](../modules/mutationFeedback.md) |
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
| [Row](../entities/TaskPostponeForm_Row.md) | Interface | 15 | — | — |
| [RowKind](../entities/RowKind.md) | Type alias | 14 | `'predecessor_accepted' \| 'linked_task' \| 'linked_triage' \| 'date' \| 'owner_decision'` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskPostponeForm` | <pre><code>&#40;&#123; task&#44; actions&#44; disabled&#44; disabledReasons &#61; &#91;&#93;&#44; onPending&#44; onUpdated &#125;&#58; &#123;&#10;    task&#58; Task&#59; actions&#58; TaskActions &#124; undefined&#59; disabled&#58; boolean&#59; &#47;&#42;&#42; Why the form cannot be used for a reason outside it&#44; such as unsaved progress&#46; &#42;&#47; disabledReasons&#63;&#58; string&#91;&#93;&#59;&#10;    onPending&#58; &#40;pending&#58; boolean&#41; &#61;&#62; void&#59; onUpdated&#58; &#40;task&#58; Task&#41; &#61;&#62; void&#59;&#10;&#125;&#41;</code></pre> | — | Postpones planned, active or resolved work with a reason and the requirements that bring it back. |
