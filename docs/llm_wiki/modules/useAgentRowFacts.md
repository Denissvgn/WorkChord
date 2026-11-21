# useAgentRowFacts Module

**Path:** `frontend/src/components/tasks/useAgentRowFacts.ts`

## Description

_Auto-generated from `frontend/src/components/tasks/useAgentRowFacts.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/agentDispatch` | `AgentDispatchState` | Declaration | erased |
| `../../features/agentDispatch` | `taskAgentDispatchState` | — | compiler-dependent |
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../types/task` | `Task`, `TaskStatus` | Declaration | erased |
| `./TaskRow` | `TaskRowAssigneeOption` | Declaration | erased |
| `@tanstack/react-query` | `useQueries` | — | compiler-dependent |
| `react` | `useMemo` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AgentRowFacts`, `DisplayedTask`, `REVIEWER_PAGE_SIZE`, `agentRowValues`, `assigneeKind`, `useAgentRowFacts` |
| Constants | `REVIEWER_PAGE_SIZE` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/projects/ProjectTaskTree.tsx"]
    n1["frontend/src/components/tasks/assigneeDisplay.test.tsx"]
    n2["frontend/src/components/tasks/TaskList.test.tsx"]
    n3["frontend/src/components/tasks/TaskList.tsx"]
    n4["frontend/src/components/tasks/TaskRow.tsx"]
    n5["frontend/src/components/tasks/useAgentRowFacts.ts"]
    n6["frontend/src/components/tasks/useTaskAssigneeDisplay.ts"]
    n7["frontend/src/features/agentDispatch.ts"]
    n8["frontend/src/pages/MyWorkPage.tsx"]
    n9["frontend/src/services/taskService.ts"]
    n10["frontend/src/types/task.ts"]
    n0 --> n4
    n0 --> n5
    n0 --> n10
    n1 --> n4
    n1 --> n5
    n1 --> n10
    n2 --> n3
    n2 --> n5
    n2 --> n10
    n3 --> n4
    n3 --> n5
    n3 --> n9
    n3 --> n10
    n4 --> n7
    n4 --> n10
    n5 --> n4
    n5 --> n7
    n5 --> n9
    n5 --> n10
    n6 --> n5
    n6 --> n9
    n6 --> n10
    n7 --> n10
    n8 --> n4
    n8 --> n5
    n8 --> n10
    n9 --> n10
    click n0 "../modules/ProjectTaskTree.md"
    click n1 "../modules/assigneeDisplay.test.md"
    click n2 "../modules/TaskList.test.md"
    click n3 "../modules/TaskList.md"
    click n4 "../modules/TaskRow.md"
    click n5 "../modules/useAgentRowFacts.md"
    click n6 "../modules/useTaskAssigneeDisplay.md"
    click n7 "../modules/agentDispatch.md"
    click n8 "../modules/MyWorkPage.md"
    click n9 "../modules/taskService.md"
    click n10 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ProjectTaskTree](../modules/ProjectTaskTree.md) |
| Inbound | [assigneeDisplay.test](../modules/assigneeDisplay.test.md) |
| Inbound | [TaskList.test](../modules/TaskList.test.md) |
| Inbound | [TaskList](../modules/TaskList.md) |
| Inbound | [useTaskAssigneeDisplay](../modules/useTaskAssigneeDisplay.md) |
| Inbound | [MyWorkPage](../modules/MyWorkPage.md) |
| Outbound | [TaskRow](../modules/TaskRow.md) |
| Outbound | [agentDispatch](../modules/agentDispatch.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [DisplayedTask](../entities/DisplayedTask.md) | Interface | 13 | — | A row the page shows: only its id and status decide whether a Reviewer is read for it. |
| [AgentRowFacts](../entities/AgentRowFacts.md) | Interface | 15 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useAgentRowFacts` | `(tasks: DisplayedTask[], known?: ReadonlyMap<number, string \| null>) -> AgentRowFacts` | — | What a task row needs beside the task to show the agent status line and the Reviewer. |
| `assigneeKind` | `(assignee: { id: number; kind?: TaskRowAssigneeOption['kind'] \| null } \| null \| undefined, option: TaskRowAssigneeOption \| undefined) -> TaskRowAssigneeOption['kind']` | — | The kind of a task's assignee: from the team read once it has the assignee's row, otherwise |
| `agentRowValues` | `(task: Pick<Task, 'id' \| 'status' \| 'agent_working' \| 'claimed_by'> & { assignee?: { id: number; kind?: TaskRowAssigneeOption['kind'] \| null } \| null }, options: TaskRowAssigneeOption[] \| undefined, facts: AgentRowFacts) -> { dispatch: AgentDispatchState \| null; reviewer: { name: string \| null } \| null \| undefined }` | — | The agent status line and the Reviewer for one row. The status line is for an agent |
