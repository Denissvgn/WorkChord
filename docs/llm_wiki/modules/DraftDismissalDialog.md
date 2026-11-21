# DraftDismissalDialog Module

**Path:** `frontend/src/components/tasks/DraftDismissalDialog.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/DraftDismissalDialog.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../common/ConfirmDialog` | `ConfirmDialog` | — | compiler-dependent |
| `../common/leaveGuardBypass` | `leaveGuardsBypassed` | — | compiler-dependent |
| `./useDraftDismissal` | `useDraftDismissal` | — | compiler-dependent |
| `react` | `useContext`, `useEffect`, `useRef` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `UNSAFE_DataRouterContext`, `useBlocker` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `DraftDismissalDialog` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/ConfirmDialog.tsx"]
    n1["frontend/src/components/common/leaveGuardBypass.ts"]
    n2["frontend/src/components/tasks/DraftDismissalDialog.tsx"]
    n3["frontend/src/components/tasks/GuardedTaskDrawer.tsx"]
    n4["frontend/src/components/tasks/TaskEditorDrawer.tsx"]
    n5["frontend/src/components/tasks/TimeEntriesPanel.tsx"]
    n6["frontend/src/components/tasks/useDraftDismissal.ts"]
    n7["frontend/src/features/firstRun/sampleProject.test.tsx"]
    n2 --> n0
    n2 --> n1
    n2 --> n6
    n3 --> n2
    n3 --> n6
    n4 --> n2
    n4 --> n6
    n5 --> n2
    n5 --> n6
    n7 --> n2
    n7 --> n6
    click n0 "../modules/ConfirmDialog.md"
    click n1 "../modules/leaveGuardBypass.md"
    click n2 "../modules/DraftDismissalDialog.md"
    click n3 "../modules/GuardedTaskDrawer.md"
    click n4 "../modules/TaskEditorDrawer.md"
    click n5 "../modules/TimeEntriesPanel.md"
    click n6 "../modules/useDraftDismissal.md"
    click n7 "../modules/sampleProject.test.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GuardedTaskDrawer](../modules/GuardedTaskDrawer.md) |
| Inbound | [TaskEditorDrawer](../modules/TaskEditorDrawer.md) |
| Inbound | [TimeEntriesPanel](../modules/TimeEntriesPanel.md) |
| Inbound | [sampleProject.test](../modules/sampleProject.test.md) |
| Outbound | [ConfirmDialog](../modules/ConfirmDialog.md) |
| Outbound | [leaveGuardBypass](../modules/leaveGuardBypass.md) |
| Outbound | [useDraftDismissal](../modules/useDraftDismissal.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [DraftGuard](../entities/DraftGuard.md) | Type alias | 8 | `ReturnType<typeof useDraftDismissal>` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `DraftDismissalDialog` | `({ guard }: { guard: DraftGuard })` | — | — |
