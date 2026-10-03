# AgentRoutingExclusion

**Location:** `frontend/src/types/agent.ts:434`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentRoutingExclusion` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `actor_id` | `number` | Yes | — | — |
| `actor_revision` | `number` | Yes | — | — |
| `actor_queue_revision` | `number` | Yes | — | — |
| `profile_id` | `number \| null` | Yes | — | — |
| `profile_revision` | `string \| null` | Yes | — | — |
| `capacity_owner_id` | `number \| null` | Yes | — | — |
| `capacity_owner_profile_id` | `number \| null` | Yes | — | — |
| `model_binding_id` | `number \| null` | Yes | — | — |
| `model_binding_revision` | `number \| null` | Yes | — | — |
| `model_catalog_id` | `number \| null` | Yes | — | — |
| `model_catalog_key` | `string \| null` | Yes | — | — |
| `model_catalog_revision` | `number \| null` | Yes | — | — |
| `configured_model_alias` | `string \| null` | Yes | — | — |
| `eligible` | `false` | Yes | — | — |
| `hard_blocker_codes` | `RoutingBlockerCode[]` | Yes | — | — |
| `matched_skill_levels` | `Record<string, TaskSkillLevel>` | Yes | — | — |
| `missing_skill_keys` | `string[]` | Yes | — | — |
| `insufficient_skill_keys` | `string[]` | Yes | — | — |
| `blocking_weakness_keys` | `string[]` | Yes | — | — |
| `reasoning_tier` | `ModelReasoningTier \| null` | Yes | — | — |
| `context_tier` | `ModelContextTier \| null` | Yes | — | — |
| `cost_tier` | `ModelCostTier \| null` | Yes | — | — |
| `latency_tier` | `ModelLatencyTier \| null` | Yes | — | — |
| `missing_modality_tags` | `string[]` | Yes | — | — |
| `missing_tool_tags` | `string[]` | Yes | — | — |
| `missing_data_policy_tags` | `string[]` | Yes | — | — |
| `available_capacity_days` | `number \| null` | Yes | — | — |
| `committed_effort_days` | `number \| null` | Yes | — | — |
| `workload_ratio` | `number \| null` | Yes | — | — |
| `vacation_conflict` | `boolean \| null` | Yes | — | — |
| `queued_assignments` | `number \| null` | Yes | — | — |
| `accepted_assignments` | `number \| null` | Yes | — | — |
| `running_runs` | `number \| null` | Yes | — | — |
| `schedule_delay_days` | `number \| null` | Yes | — | — |
| `schedule_eligible` | `boolean \| null` | Yes | — | — |
| `rationale` | `string` | Yes | — | — |

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
