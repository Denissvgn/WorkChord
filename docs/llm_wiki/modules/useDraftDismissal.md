# useDraftDismissal Module

**Path:** `frontend/src/components/tasks/useDraftDismissal.ts`

## Description

_Auto-generated from `frontend/src/components/tasks/useDraftDismissal.ts`._

Create, list edit, subtask and drawer forms share dirty/pending dismissal state. Pending work blocks unmount; declined dismissal preserves the draft. Explicit discard clears recovery storage, and clean forms close without an unnecessary prompt.

## Imports

| Source | Symbols |
|--------|---------|
| `react` | `useCallback`, `useEffect`, `useRef`, `useState` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `useDraftDismissal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/DraftDismissalDialog.tsx"]
    n1["frontend/src/components/tasks/GuardedTaskModal.tsx"]
    n2["frontend/src/components/tasks/TaskEditorDrawer.tsx"]
    n3["frontend/src/components/tasks/TimeEntriesPanel.tsx"]
    n4["frontend/src/components/tasks/useDraftDismissal.test.tsx"]
    n5["frontend/src/components/tasks/useDraftDismissal.ts"]
    n0 --> n5
    n1 --> n0
    n1 --> n5
    n2 --> n0
    n2 --> n5
    n3 --> n0
    n3 --> n5
    n4 --> n5
    click n0 "../modules/DraftDismissalDialog.md"
    click n1 "../modules/GuardedTaskModal.md"
    click n2 "../modules/TaskEditorDrawer.md"
    click n3 "../modules/TimeEntriesPanel.md"
    click n4 "../modules/useDraftDismissal.test.md"
    click n5 "../modules/useDraftDismissal.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [DraftDismissalDialog](../modules/DraftDismissalDialog.md) |
| Inbound | [GuardedTaskModal](../modules/GuardedTaskModal.md) |
| Inbound | [TaskEditorDrawer](../modules/TaskEditorDrawer.md) |
| Inbound | [TimeEntriesPanel](../modules/TimeEntriesPanel.md) |
| Inbound | [useDraftDismissal.test](../modules/useDraftDismissal.test.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useDraftDismissal` | `(onClose: () => void)` | — | — |