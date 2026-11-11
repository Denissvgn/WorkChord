# SortKey

**Location:** `frontend/src/components/tasks/TaskList.tsx:52`
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
    n1["frontend/src/components/tasks/SavedViewsControl.tsx"]
    n2["sortKeyFromSavedView (frontend/src/features/savedViews/taskViewState.ts)"]
    n3["frontend/src/pages/TasksPage.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/TaskList.md"
    click n1 "../modules/SavedViewsControl.md"
    click n2 "../modules/taskViewState.md"
    click n3 "../modules/TasksPage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [TaskList](../modules/TaskList.md) | 0 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `SavedViewsControl` | import | [SavedViewsControl](../modules/SavedViewsControl.md) | — |
| `sortKeyFromSavedView` | type_reference | [taskViewState](../modules/taskViewState.md) | — |
| `TasksPage` | import | [TasksPage](../modules/TasksPage.md) | — |
