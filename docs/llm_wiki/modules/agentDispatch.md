# agentDispatch Module

**Path:** `frontend/src/features/agentDispatch.ts`

## Description

_Auto-generated from `frontend/src/features/agentDispatch.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/task` | `Task`, `TaskStatus` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AGENT_DISPATCH_LABEL_KEY`, `AgentDispatchFacts`, `AgentDispatchState`, `agentDispatchState`, `taskAgentDispatchState` |
| Constants | `AGENT_DISPATCH_LABEL_KEY` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/TaskAssigneeDisplay.tsx"]
    n1["frontend/src/components/tasks/TaskRow.tsx"]
    n2["frontend/src/components/tasks/taskRowParts.tsx"]
    n3["frontend/src/components/tasks/useAgentRowFacts.ts"]
    n4["frontend/src/features/agentDispatch.test.ts"]
    n5["frontend/src/features/agentDispatch.ts"]
    n6["frontend/src/types/task.ts"]
    n0 --> n5
    n0 --> n6
    n1 --> n2
    n1 --> n5
    n1 --> n6
    n2 --> n5
    n3 --> n1
    n3 --> n5
    n3 --> n6
    n4 --> n5
    n5 --> n6
    click n0 "../modules/TaskAssigneeDisplay.md"
    click n1 "../modules/TaskRow.md"
    click n2 "../modules/taskRowParts.md"
    click n3 "../modules/useAgentRowFacts.md"
    click n4 "../modules/agentDispatch.test.md"
    click n5 "../modules/agentDispatch.md"
    click n6 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskAssigneeDisplay](../modules/TaskAssigneeDisplay.md) |
| Inbound | [TaskRow](../modules/TaskRow.md) |
| Inbound | [taskRowParts](../modules/taskRowParts.md) |
| Inbound | [useAgentRowFacts](../modules/useAgentRowFacts.md) |
| Inbound | [agentDispatch.test](../modules/agentDispatch.test.md) |
| Outbound | [types_task](../modules/types_task.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [AgentDispatchFacts](../entities/AgentDispatchFacts.md) | Interface | 9 | — | — |
| [AgentDispatchState](../entities/AgentDispatchState.md) | Type alias | 7 | `'noAgentConnected' \| 'notSentYet' \| 'queued' \| 'working' \| 'waitingForReview' \| 'unknown'` | Where an agent's work on a task stands, as one line under the agent's name. `unknown` is the |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `agentDispatchState` | `({ status, liveAssignment, runBegun, agentConnected }: AgentDispatchFacts) -> AgentDispatchState \| null` | — | The dispatch state of a task given to an agent, from fields the task and team APIs return. |
| `taskAgentDispatchState` | `(task: Pick<Task, 'status' \| 'agent_working' \| 'claimed_by'>, agentConnected: boolean \| undefined) -> AgentDispatchState \| null` | — | The dispatch facts a loaded task carries; whether the agent is connected comes from the team read. |
