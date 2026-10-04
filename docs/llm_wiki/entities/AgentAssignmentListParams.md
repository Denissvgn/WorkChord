# AgentAssignmentListParams

**Location:** `frontend/src/types/agent.ts:556`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentAssignmentListParams` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `taskId` | `number` | No | — | — |
| `actorId` | `number` | No | — | — |
| `purpose` | `AgentAssignmentPurpose` | No | — | — |
| `state` | `AgentAssignmentState` | No | — | — |
| `limit` | `number` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentAssignmentListParams (frontend/src/types/agent.ts)"]
    n1["frontend/src/services/agentService.ts"]
    n1 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `actorId`, `limit`, `purpose`, `state`, `taskId` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `agentService` | import | [agentService](../modules/agentService.md) | — |
