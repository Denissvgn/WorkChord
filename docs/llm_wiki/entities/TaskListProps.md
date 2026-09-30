# TaskListProps

**Location:** `frontend/src/components/tasks/TaskList.tsx:68`
**Kind:** Class
**Bases:** —
**Module:** [TaskList](../modules/TaskList.md)

## Description

_Auto-generated from `TaskListProps` in `frontend/src/components/tasks/TaskList.tsx`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `iterationId` | `number` | Yes | — | — |
| `filters` | `TaskFilters` | No | — | — |
| `sortKey` | `SortKey` | Yes | — | — |
| `onSortKeyChange` | `(sortKey: SortKey) => void` | Yes | — | — |
| `hasActiveFilters` | `boolean` | No | — | — |
| `activeViewName` | `string` | No | — | — |
| `onClearFilters` | `() => void` | No | — | — |
| `onCreateTask` | `() => void` | No | — | — |
| `requestedMode` | `TaskMode \| null` | No | — | — |
| `onModeChange` | `(mode: TaskMode \| null) => void` | No | — | — |

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
