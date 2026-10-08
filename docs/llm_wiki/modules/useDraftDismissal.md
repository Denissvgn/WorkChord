# useDraftDismissal Module

**Path:** `frontend/src/components/tasks/useDraftDismissal.ts`

## Description

Mounted-scope guards suppress obsolete close, discard and pending callbacks after an editor is removed. Existing dirty and pending confirmation, before-unload and sign-out controls retain their behavior. The reusable active-mount check also protects late write completions in task, comment and time editors.

## Imports

| Source | Symbols |
|--------|---------|
| `react` | `useCallback`, `useEffect`, `useRef`, `useState` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `useActiveMount`, `useDraftDismissal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/DraftDismissalDialog.tsx"]
    n1["frontend/src/components/tasks/GuardedTaskModal.tsx"]
    n2["frontend/src/components/tasks/TaskDiscussion.tsx"]
    n3["frontend/src/components/tasks/TaskEditorDrawer.tsx"]
    n4["frontend/src/components/tasks/TaskForm.tsx"]
    n5["frontend/src/components/tasks/TimeEntriesPanel.tsx"]
    n6["frontend/src/components/tasks/useDraftDismissal.test.tsx"]
    n7["frontend/src/components/tasks/useDraftDismissal.ts"]
    n0 --> n7
    n1 --> n0
    n1 --> n4
    n1 --> n7
    n2 --> n7
    n3 --> n0
    n3 --> n4
    n3 --> n7
    n4 --> n2
    n4 --> n5
    n4 --> n7
    n5 --> n0
    n5 --> n7
    n6 --> n7
    click n0 "../modules/DraftDismissalDialog.md"
    click n1 "../modules/GuardedTaskModal.md"
    click n2 "../modules/TaskDiscussion.md"
    click n3 "../modules/TaskEditorDrawer.md"
    click n4 "../modules/TaskForm.md"
    click n5 "../modules/TimeEntriesPanel.md"
    click n6 "../modules/useDraftDismissal.test.md"
    click n7 "../modules/useDraftDismissal.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [DraftDismissalDialog](../modules/DraftDismissalDialog.md) |
| Inbound | [GuardedTaskModal](../modules/GuardedTaskModal.md) |
| Inbound | [TaskDiscussion](../modules/TaskDiscussion.md) |
| Inbound | [TaskEditorDrawer](../modules/TaskEditorDrawer.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TimeEntriesPanel](../modules/TimeEntriesPanel.md) |
| Inbound | [useDraftDismissal.test](../modules/useDraftDismissal.test.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useActiveMount` | `()` | — | — |
| `useDraftDismissal` | `(onClose: () => void)` | — | — |