# AgentRoutingPreviewResponse

**Location:** `frontend/src/types/agent.ts:472`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentRoutingPreviewResponse` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `preview_id` | `string` | *required* | — |
| `preview_digest` | `string` | *required* | — |
| `input_digest` | `string` | *required* | — |
| `task_id` | `number` | *required* | — |
| `topology_key` | `string \| null` | *required* | — |
| `topology_revision` | `number \| null` | *required* | — |
| `purpose` | `AgentAssignmentPurpose` | *required* | — |
| `assessment_id` | `number` | *required* | — |
| `assessment_task_version` | `number` | *required* | — |
| `current_task_version` | `number` | *required* | — |
| `policy_version` | `'model-aware-routing-v1'` | *required* | — |
| `review_mode` | `TaskReviewMode` | *required* | — |
| `reviewer_profile_id` | `number \| null` | *required* | — |
| `generated_at` | `string` | *required* | — |
| `expires_at` | `string` | *required* | — |
| `recommended_candidate` | `AgentRoutingCandidate \| null` | *required* | — |
| `eligible_candidates` | `AgentRoutingCandidate[]` | *required* | — |
| `exclusions` | `AgentRoutingExclusion[]` | *required* | — |
| `eligible_candidates_omitted` | `number` | *required* | — |
| `exclusions_omitted` | `number` | *required* | — |
| `hard_blocker_codes` | `RoutingBlockerCode[]` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentRoutingPreviewResponse (frontend/src/types/agent.ts)"]
    n1["frontend/src/components/agent/RoutingCandidateComparison.tsx"]
    n2["frontend/src/components/agent/TaskRoutingPanel.test.tsx"]
    n3["frontend/src/services/agentService.ts"]
    n4["frontend/src/test/fixtures/modelAwareRouting.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/RoutingCandidateComparison.md"
    click n2 "../modules/TaskRoutingPanel.test.md"
    click n3 "../modules/agentService.md"
    click n4 "../modules/modelAwareRouting.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `assessment_id`, `assessment_task_version`, `current_task_version`, `eligible_candidates`, `eligible_candidates_omitted`, `exclusions`, `exclusions_omitted`, `expires_at`, `generated_at`, `hard_blocker_codes`, `input_digest`, `policy_version` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `RoutingCandidateComparison` | import | [RoutingCandidateComparison](../modules/RoutingCandidateComparison.md) | — |
| `TaskRoutingPanel.test` | import | [TaskRoutingPanel.test](../modules/TaskRoutingPanel.test.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
| `modelAwareRouting` | import | [modelAwareRouting](../modules/modelAwareRouting.md) | — |
