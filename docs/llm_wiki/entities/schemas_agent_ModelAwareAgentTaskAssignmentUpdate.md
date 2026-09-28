# ModelAwareAgentTaskAssignmentUpdate

**Location:** `backend/app/schemas/agent.py:592`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

PM command to reroute queued work through a fresh routing preview.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `normalize_routing_preview_id` | field | routing_preview_id | after | — |
| `normalize_routing_preview_digest` | field | routing_preview_digest | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `expected_queue_revision` | `int` | `expected_queue_revision` | Yes | No | — | ge=1 | — | — |
| `assessment_id` | `int` | `assessment_id` | Yes | No | — | ge=1 | — | — |
| `model_binding_id` | `int` | `model_binding_id` | Yes | No | — | ge=1 | — | — |
| `model_binding_revision` | `int` | `model_binding_revision` | Yes | No | — | ge=1 | — | — |
| `routing_preview_id` | `str` | `routing_preview_id` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `routing_preview_digest` | `str` | `routing_preview_digest` | Yes | No | — | max_length=64; min_length=64 | — | — |
| `actor_id` | `Optional[int]` | `actor_id` | No | Yes | `None` | ge=1 | — | — |
| `reviewer_profile_id` | `Optional[int]` | `reviewer_profile_id` | No | Yes | `None` | ge=1 | — | — |
| `queue_rank` | `Optional[int]` | `queue_rank` | No | Yes | `None` | ge=0 | — | — |
| `not_before` | `Optional[datetime]` | `not_before` | No | Yes | `None` | — | — | — |
| `state` | `Optional[Literal['queued', 'cancelled']]` | `state` | No | Yes | `None` | — | — | — |
| `reason` | `Optional[str]` | `reason` | No | Yes | `None` | max_length=unknown (MAX_AGENT_TEXT_LENGTH) | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `normalize_routing_preview_id` | `(value: str) -> str` | `@field_validator('routing_preview_id')`, `@classmethod` | — |
| `normalize_routing_preview_digest` | `(value: str) -> str` | `@field_validator('routing_preview_digest')`, `@classmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ModelAwareAgentTaskAssignmentUpdate (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["update_agent_assignment (backend/app/routers/agent.py)"]
    n4["AgentWorkService.update_assignment (backend/app/services/agent_work_service.py)"]
    n5["backend/tests/test_agent_model_catalog_api.py"]
    n6["test_completed_rework_update_persists_prior_and_new_routing_lineage (backend/tests/test_agent_routing_service.py)"]
    n7["test_completed_legacy_lineage_drops_arbitrary_private_fields (backend/tests/test_agent_routing_wave6_qualification.py)"]
    n8["test_legacy_lineage_cannot_forge_model_escalation_eligibility (backend/tests/test_agent_routing_wave6_qualification.py)"]
    n9["test_wave6_scenario_08_reasoning_rejection_permits_explicit_escalation (backend/tests/test_agent_routing_wave6_qualification.py)"]
    n10["test_wave6_scenario_09_external_blocker_cannot_escalate_model_tier (backend/tests/test_agent_routing_wave6_qualification.py)"]
    n11["backend/tests/test_agent_skill_routing_guidance.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    click n0 "../modules/schemas_agent.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_agent.md"
    click n4 "../modules/agent_work_service.md"
    click n5 "../modules/test_agent_model_catalog_api.md"
    click n6 "../modules/test_agent_routing_service.md"
    click n7 "../modules/test_agent_routing_wave6_qualification.md"
    click n8 "../modules/test_agent_routing_wave6_qualification.md"
    click n9 "../modules/test_agent_routing_wave6_qualification.md"
    click n10 "../modules/test_agent_routing_wave6_qualification.md"
    click n11 "../modules/test_agent_skill_routing_guidance.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 2 | `actor_id`, `assessment_id`, `expected_queue_revision`, `model_binding_id`, `model_binding_revision`, `not_before`, `queue_rank`, `reason`, `reviewer_profile_id`, `routing_preview_digest`, `routing_preview_id`, `state` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `update_agent_assignment` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `AgentWorkService.update_assignment` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `test_agent_model_catalog_api` | import | [test_agent_model_catalog_api](../modules/test_agent_model_catalog_api.md) | — |
| `test_completed_rework_update_persists_prior_and_new_routing_lineage` | call | [test_agent_routing_service](../modules/test_agent_routing_service.md) | 1 |
| `test_completed_legacy_lineage_drops_arbitrary_private_fields` | call | [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) | 1 |
| `test_legacy_lineage_cannot_forge_model_escalation_eligibility` | call | [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) | 1 |
| `test_wave6_scenario_08_reasoning_rejection_permits_explicit_escalation` | call | [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) | 1 |
| `test_wave6_scenario_09_external_blocker_cannot_escalate_model_tier` | call | [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) | 1 |
| `test_agent_skill_routing_guidance` | import | [test_agent_skill_routing_guidance](../modules/test_agent_skill_routing_guidance.md) | — |
