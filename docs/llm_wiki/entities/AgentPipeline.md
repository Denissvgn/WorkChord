# AgentPipeline

**Location:** `frontend/src/types/agent.ts:610`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentPipeline` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `needs_definition` | `Task[]` | Yes | — | — |
| `ready_for_agent` | `Task[]` | Yes | — | — |
| `definition_ready_unassigned` | `Task[]` | Yes | — | — |
| `assigned_waiting` | `Task[]` | Yes | — | — |
| `start_ready` | `Task[]` | Yes | — | — |
| `executing` | `Task[]` | Yes | — | — |
| `verification_required` | `Task[]` | Yes | — | — |
| `recovery_required` | `Task[]` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentPipeline (frontend/src/types/agent.ts)"]
    n1["frontend/src/pages/AgentPipelinePage.test.tsx"]
    n2["frontend/src/services/agentService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/AgentPipelinePage.test.md"
    click n2 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `assigned_waiting`, `definition_ready_unassigned`, `executing`, `needs_definition`, `ready_for_agent`, `recovery_required`, `start_ready`, `verification_required` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentPipelinePage.test` | import | [AgentPipelinePage.test](../modules/AgentPipelinePage.test.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
