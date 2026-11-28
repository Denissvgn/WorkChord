# TaskDisplayedState

**Location:** `frontend/src/types/task.ts:55`
**Kind:** Type alias
**Bases:** —
**Module:** [types_task](../modules/types_task.md)
**Target:**

```typescript
TaskStatus | TaskTerminalState
```

## Description

What a task is shown as: its stored status, or its terminal state.

## Attributes

*See the alias definition for its member types.*

## Methods

*See the alias definition for callable and member types.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskDisplayedState (frontend/src/types/task.ts)"]
    n1["frontend/src/components/analytics/StatusDistribution.tsx"]
    n2["frontend/src/components/projects/ProjectTasksTab.tsx"]
    n3["frontend/src/components/tasks/TaskList.tsx"]
    n4["frontend/src/components/tasks/TaskRow.tsx"]
    n5["isDisplayedState (frontend/src/components/ui/tone.ts)"]
    n6["frontend/src/types/iteration.ts"]
    n7["frontend/src/types/release.ts"]
    n8["stateOf (frontend/src/utils/taskState.ts)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/StatusDistribution.md"
    click n2 "../modules/ProjectTasksTab.md"
    click n3 "../modules/TaskList.md"
    click n4 "../modules/TaskRow.md"
    click n5 "../modules/tone.md"
    click n6 "../modules/types_iteration.md"
    click n7 "../modules/types_release.md"
    click n8 "../modules/taskState.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `StatusDistribution` | import | [StatusDistribution](../modules/StatusDistribution.md) | — |
| `ProjectTasksTab` | import | [ProjectTasksTab](../modules/ProjectTasksTab.md) | — |
| `TaskList` | import | [TaskList](../modules/TaskList.md) | — |
| `TaskRow` | import | [TaskRow](../modules/TaskRow.md) | — |
| `isDisplayedState` | type_reference | [tone](../modules/tone.md) | — |
| `iteration` | import | [types_iteration](../modules/types_iteration.md) | — |
| `release` | import | [types_release](../modules/types_release.md) | — |
| `stateOf` | type_reference | [taskState](../modules/taskState.md) | — |
