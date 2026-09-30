# ModelAwareAgentTaskAssignmentCreate

**Location:** `backend/app/schemas/agent.py:533`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

PM command to dispatch one preview-selected actor/model binding.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `normalize_routing_preview_id` | field | routing_preview_id | after | — |
| `normalize_routing_preview_digest` | field | routing_preview_digest | after | — |
| `validate_assignment_intent` | model | — | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `task_id` | `int` | `task_id` | Yes | No | — | ge=1 | — | — |
| `actor_id` | `int` | `actor_id` | Yes | No | — | ge=1 | — | — |
| `expected_task_version` | `int` | `expected_task_version` | Yes | No | — | ge=1 | — | — |
| `purpose` | `AgentAssignmentPurpose` | `purpose` | Yes | No | — | — | — | — |
| `assessment_id` | `int` | `assessment_id` | Yes | No | — | ge=1 | — | — |
| `model_binding_id` | `int` | `model_binding_id` | Yes | No | — | ge=1 | — | — |
| `model_binding_revision` | `int` | `model_binding_revision` | Yes | No | — | ge=1 | — | — |
| `routing_preview_id` | `str` | `routing_preview_id` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `routing_preview_digest` | `str` | `routing_preview_digest` | Yes | No | — | max_length=64; min_length=64 | — | — |
| `team_member_id` | `Optional[int]` | `team_member_id` | No | Yes | `None` | ge=1 | — | — |
| `reviewer_profile_id` | `Optional[int]` | `reviewer_profile_id` | No | Yes | `None` | ge=1 | — | — |
| `queue_class` | `AgentAssignmentQueueClass` | `queue_class` | No | No | `'normal'` | — | — | — |
| `queue_rank` | `int` | `queue_rank` | No | No | `1000` | ge=0 | — | — |
| `not_before` | `Optional[datetime]` | `not_before` | No | Yes | `None` | — | — | — |
| `reason` | `Optional[str]` | `reason` | No | Yes | `None` | max_length=unknown (MAX_AGENT_TEXT_LENGTH) | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `normalize_routing_preview_id` | `(value: str) -> str` | `@field_validator('routing_preview_id')`, `@classmethod` | — |
| `normalize_routing_preview_digest` | `(value: str) -> str` | `@field_validator('routing_preview_digest')`, `@classmethod` | — |
| `validate_assignment_intent` | `() -> 'ModelAwareAgentTaskAssignmentCreate'` | `@model_validator(mode='after')` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ModelAwareAgentTaskAssignmentCreate (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["create_agent_assignment (backend/app/routers/agent.py)"]
    n4["ModelAwareAgentTaskAssignmentCreate.validate_assignment_intent (backend/app/schemas/agent.py)"]
    n5["AgentWorkService.create_assignment (backend/app/services/agent_work_service.py)"]
    n6["backend/tests/test_agent_model_catalog_api.py"]
    n7["test_model_aware_assignment_and_begin_enforce_observed_model (backend/tests/test_agent_routing_service.py)"]
    n8["test_preview_is_deterministic_and_relevant_mutation_invalidates_it (backend/tests/test_agent_routing_service.py)"]
    n9["_dispatch (backend/tests/test_agent_routing_wave6_qualification.py)"]
    n10["backend/tests/test_agent_skill_routing_guidance.py"]
    n11["test_model_aware_commands_own_selection_and_observed_model_fields (backend/tests/test_agent_work_routing_lineage.py)"]
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
    click n4 "../modules/schemas_agent.md"
    click n5 "../modules/agent_work_service.md"
    click n6 "../modules/test_agent_model_catalog_api.md"
    click n7 "../modules/test_agent_routing_service.md"
    click n8 "../modules/test_agent_routing_service.md"
    click n9 "../modules/test_agent_routing_wave6_qualification.md"
    click n10 "../modules/test_agent_skill_routing_guidance.md"
    click n11 "../modules/test_agent_work_routing_lineage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 3 | `actor_id`, `assessment_id`, `expected_task_version`, `model_binding_id`, `model_binding_revision`, `not_before`, `purpose`, `queue_class`, `queue_rank`, `reason`, `reviewer_profile_id`, `routing_preview_digest` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `create_agent_assignment` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
| `ModelAwareAgentTaskAssignmentCreate.validate_assignment_intent` | type_reference | [schemas_agent](../modules/schemas_agent.md) | — |
| `AgentWorkService.create_assignment` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `test_agent_model_catalog_api` | import | [test_agent_model_catalog_api](../modules/test_agent_model_catalog_api.md) | — |
| `test_model_aware_assignment_and_begin_enforce_observed_model` | call | [test_agent_routing_service](../modules/test_agent_routing_service.md) | 1 |
| `test_preview_is_deterministic_and_relevant_mutation_invalidates_it` | call | [test_agent_routing_service](../modules/test_agent_routing_service.md) | 2 |
| `_dispatch` | call | [test_agent_routing_wave6_qualification](../modules/test_agent_routing_wave6_qualification.md) | 1 |
| `test_agent_skill_routing_guidance` | import | [test_agent_skill_routing_guidance](../modules/test_agent_skill_routing_guidance.md) | — |
| `test_model_aware_commands_own_selection_and_observed_model_fields` | call | [test_agent_work_routing_lineage](../modules/test_agent_work_routing_lineage.md) | 1 |
