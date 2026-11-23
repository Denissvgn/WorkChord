# AgentDispatchFacts

**Location:** `frontend/src/features/agentDispatch.ts:9`
**Kind:** Interface
**Bases:** —
**Module:** [agentDispatch](../modules/agentDispatch.md)

## Description

_Auto-generated from `AgentDispatchFacts` in `frontend/src/features/agentDispatch.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `status` | `TaskStatus` | Yes | — | — |
| `liveAssignment` | `boolean \| null` | No | — | — |
| `runBegun` | `boolean` | Yes | — | — |
| `agentConnected` | `boolean` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentDispatchFacts (frontend/src/features/agentDispatch.ts)"]
    n1["frontend/src/features/agentDispatch.test.ts"]
    n2["agentDispatchState (frontend/src/features/agentDispatch.ts)"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/agentDispatch.md"
    click n1 "../modules/agentDispatch.test.md"
    click n2 "../modules/agentDispatch.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agentDispatch](../modules/agentDispatch.md) | 0 | `agentConnected`, `liveAssignment`, `runBegun`, `status` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `agentDispatch.test` | import | [agentDispatch.test](../modules/agentDispatch.test.md) | — |
| `agentDispatchState` | type_reference | [agentDispatch](../modules/agentDispatch.md) | — |
