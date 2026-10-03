# TaskRoutingAssessmentCommand

**Location:** `frontend/src/types/agent.ts:325`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `TaskRoutingAssessmentCommand` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `expected_task_version` | `number` | Yes | — | — |
| `band` | `TaskDifficultyBand` | Yes | — | — |
| `axes` | `TaskDifficultyAxes` | Yes | — | — |
| `required_skill_levels` | `Record<string, TaskSkillLevel>` | Yes | — | — |
| `required_model` | `RequiredModelEnvelope` | Yes | — | — |
| `review_mode` | `TaskReviewMode` | Yes | — | — |
| `confidence` | `number` | Yes | — | — |
| `reason_codes` | `AssessmentReasonCode[]` | Yes | — | — |
| `rationale` | `string` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskRoutingAssessmentCommand (frontend/src/types/agent.ts)"]
    n1["frontend/src/components/agent/TaskRoutingPanel.tsx"]
    n2["frontend/src/services/agentService.test.ts"]
    n3["frontend/src/services/agentService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/TaskRoutingPanel.md"
    click n2 "../modules/agentService.test.md"
    click n3 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `axes`, `band`, `confidence`, `expected_task_version`, `rationale`, `reason_codes`, `required_model`, `required_skill_levels`, `review_mode` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskRoutingPanel` | import | [TaskRoutingPanel](../modules/TaskRoutingPanel.md) | — |
| `agentService.test` | import | [agentService.test](../modules/agentService.test.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
