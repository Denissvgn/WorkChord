# AgentDispatchState

**Location:** `frontend/src/features/agentDispatch.ts:7`
**Kind:** Type alias
**Bases:** —
**Module:** [agentDispatch](../modules/agentDispatch.md)
**Target:**

```typescript
'noAgentConnected' | 'notSentYet' | 'queued' | 'working' | 'waitingForReview' | 'unknown'
```

## Description

Where an agent's work on a task stands, as one line under the agent's name. `unknown` is the
neutral line while the reads that say whether the agent is connected are loading or failed.

## Attributes

*See the alias definition for its member types.*

## Methods

*See the alias definition for callable and member types.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentDispatchState (frontend/src/features/agentDispatch.ts)"]
    n1["frontend/src/components/tasks/TaskRow.tsx"]
    n2["AgentDispatchLine (frontend/src/components/tasks/taskRowParts.tsx)"]
    n3["agentRowValues (frontend/src/components/tasks/useAgentRowFacts.ts)"]
    n4["agentDispatchState (frontend/src/features/agentDispatch.ts)"]
    n5["taskAgentDispatchState (frontend/src/features/agentDispatch.ts)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/agentDispatch.md"
    click n1 "../modules/TaskRow.md"
    click n2 "../modules/taskRowParts.md"
    click n3 "../modules/useAgentRowFacts.md"
    click n4 "../modules/agentDispatch.md"
    click n5 "../modules/agentDispatch.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agentDispatch](../modules/agentDispatch.md) | 0 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskRow` | import | [TaskRow](../modules/TaskRow.md) | — |
| `AgentDispatchLine` | type_reference | [taskRowParts](../modules/taskRowParts.md) | — |
| `agentRowValues` | type_reference | [useAgentRowFacts](../modules/useAgentRowFacts.md) | — |
| `agentDispatchState` | type_reference | [agentDispatch](../modules/agentDispatch.md) | — |
| `taskAgentDispatchState` | type_reference | [agentDispatch](../modules/agentDispatch.md) | — |
