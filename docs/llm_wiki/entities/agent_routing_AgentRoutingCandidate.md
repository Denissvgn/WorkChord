# AgentRoutingCandidate

**Location:** `backend/app/schemas/agent_routing.py:926`
**Kind:** Pydantic model
**Bases:** `RoutingContractModel`
**Module:** [agent_routing](../modules/agent_routing.md)

## Description

One eligible actor plus exact model-binding candidate.

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `validate_matched_skills` | field | matched_skill_levels | before | — |
| `validate_capability_tags` | field | modality_tags, tool_tags, data_policy_tags | after | — |
| `strip_candidate_text` | field | profile_revision, configured_model_alias, rationale | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `actor_id` | `int` | `actor_id` | Yes | No | — | ge=1; strict=True | — | — |
| `actor_revision` | `PositiveRevision` | `actor_revision` | Yes | No | — | — | — | — |
| `actor_queue_revision` | `PositiveRevision` | `actor_queue_revision` | Yes | No | — | — | — | — |
| `profile_id` | `int` | `profile_id` | Yes | No | — | ge=1; strict=True | — | — |
| `profile_revision` | `str` | `profile_revision` | Yes | No | — | max_length=120; min_length=1 | — | — |
| `capacity_owner_id` | `int \| None` | `capacity_owner_id` | No | Yes | `None` | ge=1; strict=True | — | — |
| `capacity_owner_profile_id` | `int \| None` | `capacity_owner_profile_id` | No | Yes | `None` | ge=1; strict=True | — | — |
| `model_binding_id` | `int` | `model_binding_id` | Yes | No | — | ge=1; strict=True | — | — |
| `model_binding_revision` | `PositiveRevision` | `model_binding_revision` | Yes | No | — | — | — | — |
| `model_catalog_id` | `int` | `model_catalog_id` | Yes | No | — | ge=1; strict=True | — | — |
| `model_catalog_key` | `RoutingKey` | `model_catalog_key` | Yes | No | — | — | — | — |
| `model_catalog_revision` | `PositiveRevision` | `model_catalog_revision` | Yes | No | — | — | — | — |
| `configured_model_alias` | `str` | `configured_model_alias` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `eligible` | `Literal[True]` | `eligible` | No | No | `True` | — | — | — |
| `hard_blocker_codes` | `list[RoutingBlockerCode]` | `hard_blocker_codes` | No | No | factory: `list` | max_length=0 | — | — |
| `matched_skill_levels` | `dict[str, SkillLevel]` | `matched_skill_levels` | No | No | factory: `dict` | — | — | — |
| `missing_skill_keys` | `list[RoutingKey]` | `missing_skill_keys` | No | No | factory: `list` | max_length=0 | — | — |
| `blocking_weakness_keys` | `list[RoutingKey]` | `blocking_weakness_keys` | No | No | factory: `list` | max_length=0 | — | — |
| `reasoning_tier` | `ReasoningTier` | `reasoning_tier` | Yes | No | — | — | — | — |
| `context_tier` | `ModelContextTier` | `context_tier` | Yes | No | — | — | — | — |
| `modality_tags` | `list[str]` | `modality_tags` | No | No | factory: `list` | — | — | — |
| `tool_tags` | `list[str]` | `tool_tags` | No | No | factory: `list` | — | — | — |
| `data_policy_tags` | `list[str]` | `data_policy_tags` | No | No | factory: `list` | — | — | — |
| `cost_tier` | `ModelCostTier` | `cost_tier` | Yes | No | — | — | — | — |
| `latency_tier` | `ModelLatencyTier` | `latency_tier` | Yes | No | — | — | — | — |
| `available_capacity_days` | `float` | `available_capacity_days` | Yes | No | — | ge=0 | — | — |
| `committed_effort_days` | `float` | `committed_effort_days` | Yes | No | — | ge=0 | — | — |
| `workload_ratio` | `float` | `workload_ratio` | Yes | No | — | ge=0 | — | — |
| `vacation_conflict` | `Literal[False]` | `vacation_conflict` | No | No | `False` | — | — | — |
| `queued_assignments` | `int` | `queued_assignments` | Yes | No | — | ge=0; strict=True | — | — |
| `accepted_assignments` | `int` | `accepted_assignments` | Yes | No | — | ge=0; strict=True | — | — |
| `running_runs` | `int` | `running_runs` | Yes | No | — | ge=0; strict=True | — | — |
| `schedule_delay_days` | `float` | `schedule_delay_days` | Yes | No | — | ge=0 | — | — |
| `schedule_eligible` | `Literal[True]` | `schedule_eligible` | No | No | `True` | — | — | — |
| `adequacy_class` | `int` | `adequacy_class` | Yes | No | — | ge=0; strict=True | — | — |
| `rank` | `int` | `rank` | Yes | No | — | ge=1; strict=True | — | — |
| `confidence` | `float` | `confidence` | Yes | No | — | le=1.0; ge=unknown (MIN_ROUTING_ASSESSMENT_CONFIDENCE) | — | — |
| `rationale` | `str` | `rationale` | Yes | No | — | max_length=2000; min_length=1 | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `validate_matched_skills` | `(value: Any) -> Any` | `@field_validator('matched_skill_levels', mode='before')`, `@classmethod` | — |
| `validate_capability_tags` | `(value: list[str], info: Any) -> list[str]` | `@field_validator('modality_tags', 'tool_tags', 'data_policy_tags')`, `@classmethod` | — |
| `strip_candidate_text` | `(value: str) -> str` | `@field_validator('profile_revision', 'configured_model_alias', 'rationale')`, `@classmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentRoutingCandidate (backend/app/schemas/agent_routing.py)"]
    n1["RoutingContractModel (backend/app/schemas/agent_routing.py)"]
    n2["backend/app/services/agent_routing_service.py"]
    n3["_candidate (backend/tests/test_agent_routing_wave3_contract.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/agent_routing.md"
    click n1 "../modules/agent_routing.md"
    click n2 "../modules/agent_routing_service.md"
    click n3 "../modules/test_agent_routing_wave3_contract.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing](../modules/agent_routing.md) | 3 | `accepted_assignments`, `actor_id`, `actor_queue_revision`, `actor_revision`, `adequacy_class`, `available_capacity_days`, `blocking_weakness_keys`, `capacity_owner_id`, `capacity_owner_profile_id`, `committed_effort_days`, `confidence`, `configured_model_alias` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RoutingContractModel` | [agent_routing](../modules/agent_routing.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `agent_routing_service` | import | [agent_routing_service](../modules/agent_routing_service.md) | — |
| `_candidate` | type_reference | [test_agent_routing_wave3_contract](../modules/test_agent_routing_wave3_contract.md) | — |
