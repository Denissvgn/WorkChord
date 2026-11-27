# MutationSuccessFeedback Module

**Path:** `frontend/src/features/MutationSuccessFeedback.tsx`

## Description

_Auto-generated from `frontend/src/features/MutationSuccessFeedback.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/feedback/toast` | `useToast` | — | compiler-dependent |
| `../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `./mutationFeedback` | `MutationFeedbackMeta` | Declaration | erased |
| `@tanstack/react-query` | `useQueryClient` | — | compiler-dependent |
| `react` | `useEffect` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `MutationSuccessFeedback` |
| Constants | `UNDO_TOAST_MS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/feedback/toast.ts"]
    n1["frontend/src/components/settings/TemplateLabelSettings.test.tsx"]
    n2["frontend/src/components/tasks/TaskBulkReassign.test.tsx"]
    n3["frontend/src/components/tasks/TaskOwnerAcceptance.test.tsx"]
    n4["frontend/src/components/tasks/TaskPostponement.test.tsx"]
    n5["frontend/src/features/identity/IdentityProvider.tsx"]
    n6["frontend/src/features/mutationFeedback.test.tsx"]
    n7["frontend/src/features/mutationFeedback.ts"]
    n8["frontend/src/features/MutationSuccessFeedback.tsx"]
    n9["frontend/src/utils/apiError.ts"]
    n1 --> n8
    n2 --> n8
    n3 --> n8
    n4 --> n8
    n5 --> n8
    n5 --> n9
    n6 --> n7
    n6 --> n8
    n8 --> n0
    n8 --> n7
    n8 --> n9
    click n0 "../modules/toast.md"
    click n1 "../modules/TemplateLabelSettings.test.md"
    click n2 "../modules/TaskBulkReassign.test.md"
    click n3 "../modules/TaskOwnerAcceptance.test.md"
    click n4 "../modules/TaskPostponement.test.md"
    click n5 "../modules/IdentityProvider.md"
    click n6 "../modules/mutationFeedback.test.md"
    click n7 "../modules/mutationFeedback.md"
    click n8 "../modules/MutationSuccessFeedback.md"
    click n9 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TemplateLabelSettings.test](../modules/TemplateLabelSettings.test.md) |
| Inbound | [TaskBulkReassign.test](../modules/TaskBulkReassign.test.md) |
| Inbound | [TaskOwnerAcceptance.test](../modules/TaskOwnerAcceptance.test.md) |
| Inbound | [TaskPostponement.test](../modules/TaskPostponement.test.md) |
| Inbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Inbound | [mutationFeedback.test](../modules/mutationFeedback.test.md) |
| Outbound | [toast](../modules/toast.md) |
| Outbound | [mutationFeedback](../modules/mutationFeedback.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `MutationSuccessFeedback` | `()` | — | Shows the success toast declared by each mutation's `meta`. Mount once inside the work query client. |
