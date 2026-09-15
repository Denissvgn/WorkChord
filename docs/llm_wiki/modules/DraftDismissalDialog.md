# DraftDismissalDialog Module

**Path:** `frontend/src/components/tasks/DraftDismissalDialog.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/DraftDismissalDialog.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../common/ConfirmDialog` | `ConfirmDialog` |
| `./useDraftDismissal` | `useDraftDismissal` |
| `react` | `useContext`, `useEffect` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `UNSAFE_DataRouterContext`, `useBlocker` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `DraftDismissalDialog` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/ConfirmDialog.tsx"]
    n1["frontend/src/components/tasks/DraftDismissalDialog.tsx"]
    n2["frontend/src/components/tasks/GuardedTaskModal.tsx"]
    n3["frontend/src/components/tasks/TaskEditorDrawer.tsx"]
    n4["frontend/src/components/tasks/useDraftDismissal.ts"]
    n1 --> n0
    n1 --> n4
    n2 --> n1
    n2 --> n4
    n3 --> n1
    n3 --> n4
    click n0 "../modules/ConfirmDialog.md"
    click n1 "../modules/DraftDismissalDialog.md"
    click n2 "../modules/GuardedTaskModal.md"
    click n3 "../modules/TaskEditorDrawer.md"
    click n4 "../modules/useDraftDismissal.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GuardedTaskModal](../modules/GuardedTaskModal.md) |
| Inbound | [TaskEditorDrawer](../modules/TaskEditorDrawer.md) |
| Outbound | [ConfirmDialog](../modules/ConfirmDialog.md) |
| Outbound | [useDraftDismissal](../modules/useDraftDismissal.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [DraftGuard](../entities/DraftGuard.md) | Type alias | 7 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `DraftDismissalDialog` | `({ guard }: { guard: DraftGuard })` | — | — |
