# TaskDiscussion Module

**Path:** `frontend/src/components/tasks/TaskDiscussion.tsx`

## Description

Keeps discussion distinct from execution and acceptance. Plain-text comments preserve authorship, versioned edits and history. Same-account drafts retain edit identity and mentions; conflicts require an explicit current-version comparison. Subscription settings, pending states and errors remain visible without dismissing the task editor.

## Imports

| Source | Symbols |
|--------|---------|
| `../../features/identity/identityContext` | `useIdentity` |
| `../../services/discussionService` | `discussionService`, `TaskComment` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../common/Button` | `Button` |
| `../feedback/QueryState` | `QueryErrorState` |
| `@tanstack/react-query` | `useInfiniteQuery`, `useMutation`, `useQuery` |
| `react` | `useEffect`, `useId`, `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskDiscussion` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/components/tasks/TaskDiscussion.test.tsx"]
    n3["frontend/src/components/tasks/TaskDiscussion.tsx"]
    n4["frontend/src/components/tasks/TaskForm.tsx"]
    n5["frontend/src/features/identity/identityContext.ts"]
    n6["frontend/src/services/discussionService.ts"]
    n7["frontend/src/utils/apiError.ts"]
    n1 --> n0
    n1 --> n7
    n2 --> n3
    n2 --> n5
    n3 --> n0
    n3 --> n1
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n4 --> n0
    n4 --> n1
    n4 --> n3
    n4 --> n5
    n4 --> n7
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/TaskDiscussion.test.md"
    click n3 "../modules/TaskDiscussion.md"
    click n4 "../modules/TaskForm.md"
    click n5 "../modules/identityContext.md"
    click n6 "../modules/discussionService.md"
    click n7 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskDiscussion.test](../modules/TaskDiscussion.test.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [discussionService](../modules/discussionService.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [EditingComment](../entities/EditingComment.md) | Type alias | 11 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskDiscussion` | `({ taskId, draftKey, disabled, onDirty, onPending }: {     taskId: number; draftKey: string \| null; disabled: boolean;     onDirty: (dirty: boolean) => void; onPending: (pending: boolean) => void; })` | — | — |
