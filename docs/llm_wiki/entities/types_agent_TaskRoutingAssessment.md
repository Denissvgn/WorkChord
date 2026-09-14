# TaskRoutingAssessment

**Location:** `frontend/src/types/agent.ts:336`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `TaskRoutingAssessment` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `number` | *required* | — |
| `task_id` | `number` | *required* | — |
| `task_version` | `number` | *required* | — |
| `policy_version` | `'model-aware-routing-v1'` | *required* | — |
| `band` | `TaskDifficultyBand` | *required* | — |
| `axes` | `TaskDifficultyAxes` | *required* | — |
| `required_skill_levels` | `Record<string, number>` | *required* | — |
| `required_model` | `RequiredModelEnvelope` | *required* | — |
| `review_mode` | `TaskReviewMode` | *required* | — |
| `confidence` | `number` | *required* | — |
| `reason_codes` | `string[]` | *required* | — |
| `rationale` | `string` | *required* | — |
| `assessor` | `string` | *required* | — |
| `assessor_actor_id` | `number \| null` | *required* | — |
| `created_at` | `string` | *required* | — |
| `policy_conformant` | `boolean` | *required* | — |
| `is_current` | `boolean` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskRoutingAssessment (frontend/src/types/agent.ts)"]
    n1["frontend/src/components/agent/TaskRoutingPanel.test.tsx"]
    n2["frontend/src/components/agent/TaskRoutingPanel.tsx"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/TaskRoutingPanel.test.md"
    click n2 "../modules/TaskRoutingPanel.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `assessor`, `assessor_actor_id`, `axes`, `band`, `confidence`, `created_at`, `id`, `is_current`, `policy_conformant`, `policy_version`, `rationale`, `reason_codes` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskRoutingPanel.test` | import | [TaskRoutingPanel.test](../modules/TaskRoutingPanel.test.md) | — |
| `TaskRoutingPanel` | import | [TaskRoutingPanel](../modules/TaskRoutingPanel.md) | — |
