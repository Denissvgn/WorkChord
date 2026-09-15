# TaskListProps

**Location:** `frontend/src/components/tasks/TaskList.tsx:66`
**Kind:** Class
**Bases:** —
**Module:** [TaskList](../modules/TaskList.md)

## Description

_Auto-generated from `TaskListProps` in `frontend/src/components/tasks/TaskList.tsx`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `iterationId` | `number` | *required* | — |
| `filters` | `TaskFilters` | *required* | — |
| `sortKey` | `SortKey` | *required* | — |
| `onSortKeyChange` | `(sortKey: SortKey) => void` | *required* | — |
| `hasActiveFilters` | `boolean` | *required* | — |
| `activeViewName` | `string` | *required* | — |
| `onClearFilters` | `() => void` | *required* | — |
| `onCreateTask` | `() => void` | *required* | — |
| `requestedMode` | `TaskMode \| null` | *required* | — |
| `onModeChange` | `(mode: TaskMode \| null) => void` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskListProps (frontend/src/components/tasks/TaskList.tsx)"]
    n1["TaskList (frontend/src/components/tasks/TaskList.tsx)"]
    n1 --> n0
    click n0 "../modules/TaskList.md"
    click n1 "../modules/TaskList.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [TaskList](../modules/TaskList.md) | 0 | `activeViewName`, `filters`, `hasActiveFilters`, `iterationId`, `onClearFilters`, `onCreateTask`, `onModeChange`, `onSortKeyChange`, `requestedMode`, `sortKey` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskList` | type_reference | [TaskList](../modules/TaskList.md) | — |
