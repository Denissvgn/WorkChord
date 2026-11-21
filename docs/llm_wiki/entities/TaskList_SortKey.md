# SortKey

**Location:** `frontend/src/components/tasks/TaskList.tsx:64`
**Kind:** Type alias
**Bases:** —
**Module:** [TaskList](../modules/TaskList.md)
**Target:**

```typescript
'priority' | 'sort_order' | 'status' | 'title'
```

## Description

_Auto-generated from `SortKey` in `frontend/src/components/tasks/TaskList.tsx`._

## Attributes

*See the alias definition for its member types.*

## Methods

*See the alias definition for callable and member types.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SortKey (frontend/src/components/tasks/TaskList.tsx)"]
    n1["TaskViewOptions (frontend/src/components/tasks/TaskViewOptions.tsx)"]
    n2["frontend/src/components/tasks/useSavedViewManager.tsx"]
    n3["sortKeyFromSearchParams (frontend/src/features/savedViews/taskViewParams.ts)"]
    n4["writeSortKeyToSearchParams (frontend/src/features/savedViews/taskViewParams.ts)"]
    n5["sortKeyFromSavedView (frontend/src/features/savedViews/taskViewState.ts)"]
    n6["frontend/src/pages/TasksPage.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/TaskList.md"
    click n1 "../modules/TaskViewOptions.md"
    click n2 "../modules/useSavedViewManager.md"
    click n3 "../modules/taskViewParams.md"
    click n4 "../modules/taskViewParams.md"
    click n5 "../modules/taskViewState.md"
    click n6 "../modules/TasksPage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [TaskList](../modules/TaskList.md) | 0 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskViewOptions` | type_reference | [TaskViewOptions](../modules/TaskViewOptions.md) | — |
| `useSavedViewManager` | import | [useSavedViewManager](../modules/useSavedViewManager.md) | — |
| `sortKeyFromSearchParams` | type_reference | [taskViewParams](../modules/taskViewParams.md) | — |
| `writeSortKeyToSearchParams` | type_reference | [taskViewParams](../modules/taskViewParams.md) | — |
| `sortKeyFromSavedView` | type_reference | [taskViewState](../modules/taskViewState.md) | — |
| `TasksPage` | import | [TasksPage](../modules/TasksPage.md) | — |
