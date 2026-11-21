# TaskTimelineResponse

**Location:** `frontend/src/types/agent.ts:654`
**Kind:** Interface
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `TaskTimelineResponse` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `task_id` | `number` | Yes | — | — |
| `items` | `TaskTimelineItem[]` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskTimelineResponse (frontend/src/types/agent.ts)"]
    n1["frontend/src/pages/PipelineTaskEvidence.test.tsx"]
    n2["frontend/src/services/agentService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/PipelineTaskEvidence.test.md"
    click n2 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `items`, `task_id` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `PipelineTaskEvidence.test` | import | [PipelineTaskEvidence.test](../modules/PipelineTaskEvidence.test.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
