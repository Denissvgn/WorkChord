# TaskDiscussion Module

**Path:** `frontend/src/components/tasks/TaskDiscussion.tsx`

## Description

Keeps discussion distinct from execution and acceptance. Plain-text comments preserve authorship, versioned edits and history. Same-account drafts retain edit identity and mentions; conflicts require an explicit current-version comparison. Subscription settings, pending states and errors remain visible without dismissing the task editor.

Comment drafts checkpoint uncertainty before writing and retain input through missing responses. A current read and explicit comparison are required to resume; confirmed version conflicts retain the original edit observation until deliberate reapplication. Operation markers prevent obsolete acknowledgments from clearing newer local input.

## Imports

| Source | Symbols |
|--------|---------|
| `../../components/feedback/LiveWindowStatus` | `LiveWindowStatus` |
| `../../features/identity/identityContext` | `useIdentity` |
| `../../features/useLiveWindow` | `useLiveWindow` |
| `../../services/discussionService` | `discussionService`, `TaskComment` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../common/Button` | `Button` |
| `../feedback/QueryState` | `QueryErrorState` |
| `./useDraftDismissal` | `useActiveMount` |
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
    n1["frontend/src/components/feedback/LiveWindowStatus.tsx"]
    n2["frontend/src/components/feedback/QueryState.tsx"]
    n3["frontend/src/components/tasks/TaskDiscussion.test.tsx"]
    n4["frontend/src/components/tasks/TaskDiscussion.tsx"]
    n5["frontend/src/components/tasks/TaskForm.tsx"]
    n6["frontend/src/components/tasks/useDraftDismissal.ts"]
    n7["frontend/src/features/identity/identityContext.ts"]
    n8["frontend/src/features/useLiveWindow.ts"]
    n9["frontend/src/services/discussionService.ts"]
    n10["frontend/src/utils/apiError.ts"]
    n1 --> n0
    n2 --> n0
    n2 --> n10
    n3 --> n4
    n3 --> n7
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n4 --> n9
    n4 --> n10
    n5 --> n0
    n5 --> n2
    n5 --> n4
    n5 --> n6
    n5 --> n7
    n5 --> n10
    click n0 "../modules/Button.md"
    click n1 "../modules/LiveWindowStatus.md"
    click n2 "../modules/QueryState.md"
    click n3 "../modules/TaskDiscussion.test.md"
    click n4 "../modules/TaskDiscussion.md"
    click n5 "../modules/TaskForm.md"
    click n6 "../modules/useDraftDismissal.md"
    click n7 "../modules/identityContext.md"
    click n8 "../modules/useLiveWindow.md"
    click n9 "../modules/discussionService.md"
    click n10 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskDiscussion.test](../modules/TaskDiscussion.test.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [LiveWindowStatus](../modules/LiveWindowStatus.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [useDraftDismissal](../modules/useDraftDismissal.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [useLiveWindow](../modules/useLiveWindow.md) |
| Outbound | [discussionService](../modules/discussionService.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [EditingComment](../entities/EditingComment.md) | Type alias | 14 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskDiscussion` | `({ taskId, draftKey, disabled, onDirty, onPending }: {     taskId: number; draftKey: string \| null; disabled: boolean;     onDirty: (dirty: boolean) => void; onPending: (pending: boolean) => void; })` | — | — |