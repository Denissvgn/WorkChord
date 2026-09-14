# AgentRoutingExclusion

**Location:** `frontend/src/types/agent.ts:433`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentRoutingExclusion` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `actor_id` | `number` | *required* | — |
| `actor_revision` | `number` | *required* | — |
| `actor_queue_revision` | `number` | *required* | — |
| `profile_id` | `number \| null` | *required* | — |
| `profile_revision` | `string \| null` | *required* | — |
| `capacity_owner_id` | `number \| null` | *required* | — |
| `capacity_owner_profile_id` | `number \| null` | *required* | — |
| `model_binding_id` | `number \| null` | *required* | — |
| `model_binding_revision` | `number \| null` | *required* | — |
| `model_catalog_id` | `number \| null` | *required* | — |
| `model_catalog_key` | `string \| null` | *required* | — |
| `model_catalog_revision` | `number \| null` | *required* | — |
| `configured_model_alias` | `string \| null` | *required* | — |
| `eligible` | `false` | *required* | — |
| `hard_blocker_codes` | `RoutingBlockerCode[]` | *required* | — |
| `matched_skill_levels` | `Record<string, TaskSkillLevel>` | *required* | — |
| `missing_skill_keys` | `string[]` | *required* | — |
| `insufficient_skill_keys` | `string[]` | *required* | — |
| `blocking_weakness_keys` | `string[]` | *required* | — |
| `reasoning_tier` | `ModelReasoningTier \| null` | *required* | — |
| `context_tier` | `ModelContextTier \| null` | *required* | — |
| `cost_tier` | `ModelCostTier \| null` | *required* | — |
| `latency_tier` | `ModelLatencyTier \| null` | *required* | — |
| `missing_modality_tags` | `string[]` | *required* | — |
| `missing_tool_tags` | `string[]` | *required* | — |
| `missing_data_policy_tags` | `string[]` | *required* | — |
| `available_capacity_days` | `number \| null` | *required* | — |
| `committed_effort_days` | `number \| null` | *required* | — |
| `workload_ratio` | `number \| null` | *required* | — |
| `vacation_conflict` | `boolean \| null` | *required* | — |
| `queued_assignments` | `number \| null` | *required* | — |
| `accepted_assignments` | `number \| null` | *required* | — |
| `running_runs` | `number \| null` | *required* | — |
| `schedule_delay_days` | `number \| null` | *required* | — |
| `schedule_eligible` | `boolean \| null` | *required* | — |
| `rationale` | `string` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentRoutingExclusion (frontend/src/types/agent.ts)"]
    n1["frontend/src/components/agent/RoutingCandidateComparison.tsx"]
    n2["frontend/src/test/fixtures/modelAwareRouting.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/RoutingCandidateComparison.md"
    click n2 "../modules/modelAwareRouting.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `accepted_assignments`, `actor_id`, `actor_queue_revision`, `actor_revision`, `available_capacity_days`, `blocking_weakness_keys`, `capacity_owner_id`, `capacity_owner_profile_id`, `committed_effort_days`, `configured_model_alias`, `context_tier`, `cost_tier` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `RoutingCandidateComparison` | import | [RoutingCandidateComparison](../modules/RoutingCandidateComparison.md) | — |
| `modelAwareRouting` | import | [modelAwareRouting](../modules/modelAwareRouting.md) | — |
