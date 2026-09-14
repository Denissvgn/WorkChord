# AgentRoutingCandidate

**Location:** `frontend/src/types/agent.ts:392`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentRoutingCandidate` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `actor_id` | `number` | *required* | — |
| `actor_revision` | `number` | *required* | — |
| `actor_queue_revision` | `number` | *required* | — |
| `profile_id` | `number` | *required* | — |
| `profile_revision` | `string` | *required* | — |
| `capacity_owner_id` | `number \| null` | *required* | — |
| `capacity_owner_profile_id` | `number \| null` | *required* | — |
| `model_binding_id` | `number` | *required* | — |
| `model_binding_revision` | `number` | *required* | — |
| `model_catalog_id` | `number` | *required* | — |
| `model_catalog_key` | `string` | *required* | — |
| `model_catalog_revision` | `number` | *required* | — |
| `configured_model_alias` | `string` | *required* | — |
| `eligible` | `true` | *required* | — |
| `hard_blocker_codes` | `RoutingBlockerCode[]` | *required* | — |
| `matched_skill_levels` | `Record<string, TaskSkillLevel>` | *required* | — |
| `missing_skill_keys` | `string[]` | *required* | — |
| `blocking_weakness_keys` | `string[]` | *required* | — |
| `reasoning_tier` | `ModelReasoningTier` | *required* | — |
| `context_tier` | `ModelContextTier` | *required* | — |
| `modality_tags` | `string[]` | *required* | — |
| `tool_tags` | `string[]` | *required* | — |
| `data_policy_tags` | `string[]` | *required* | — |
| `cost_tier` | `ModelCostTier` | *required* | — |
| `latency_tier` | `ModelLatencyTier` | *required* | — |
| `available_capacity_days` | `number` | *required* | — |
| `committed_effort_days` | `number` | *required* | — |
| `workload_ratio` | `number` | *required* | — |
| `vacation_conflict` | `false` | *required* | — |
| `queued_assignments` | `number` | *required* | — |
| `accepted_assignments` | `number` | *required* | — |
| `running_runs` | `number` | *required* | — |
| `schedule_delay_days` | `number` | *required* | — |
| `schedule_eligible` | `true` | *required* | — |
| `adequacy_class` | `number` | *required* | — |
| `rank` | `number` | *required* | — |
| `confidence` | `number` | *required* | — |
| `rationale` | `string` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentRoutingCandidate (frontend/src/types/agent.ts)"]
    n1["frontend/src/components/agent/RoutingCandidateComparison.tsx"]
    n2["frontend/src/components/agent/TaskRoutingPanel.tsx"]
    n3["frontend/src/test/fixtures/modelAwareRouting.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/RoutingCandidateComparison.md"
    click n2 "../modules/TaskRoutingPanel.md"
    click n3 "../modules/modelAwareRouting.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `accepted_assignments`, `actor_id`, `actor_queue_revision`, `actor_revision`, `adequacy_class`, `available_capacity_days`, `blocking_weakness_keys`, `capacity_owner_id`, `capacity_owner_profile_id`, `committed_effort_days`, `confidence`, `configured_model_alias` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `RoutingCandidateComparison` | import | [RoutingCandidateComparison](../modules/RoutingCandidateComparison.md) | — |
| `TaskRoutingPanel` | import | [TaskRoutingPanel](../modules/TaskRoutingPanel.md) | — |
| `modelAwareRouting` | import | [modelAwareRouting](../modules/modelAwareRouting.md) | — |
