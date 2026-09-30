# AgentCommandMetadata

**Location:** `frontend/src/types/agent.ts:94`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentCommandMetadata` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `idempotencyKey` | `string` | Yes | — | — |
| `rationale` | `string` | Yes | — | — |
| `correlationId` | `string` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentCommandMetadata (frontend/src/types/agent.ts)"]
    n1["frontend/src/services/agentService.test.ts"]
    n2["frontend/src/services/agentService.ts"]
    n3["createAgentCommandMetadata (frontend/src/utils/modelRouting.ts)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/agentService.test.md"
    click n2 "../modules/agentService.md"
    click n3 "../modules/modelRouting.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `correlationId`, `idempotencyKey`, `rationale` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `agentService.test` | import | [agentService.test](../modules/agentService.test.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
| `createAgentCommandMetadata` | type_reference | [modelRouting](../modules/modelRouting.md) | — |
