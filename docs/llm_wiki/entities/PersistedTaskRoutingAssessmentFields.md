# PersistedTaskRoutingAssessmentFields

**Location:** `backend/app/schemas/agent_routing.py:658`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [agent_routing](../modules/agent_routing.md)

## Description

Backward-compatible decoder for rows written under the original v1 schema.

New writes use ``TaskRoutingAssessmentCreate`` and its stricter deterministic
policy. Existing append-only v1 rows retain the validation rules that were
active when they were accepted, so reading them cannot retroactively fail.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |
| `from_attributes` | `True` | model_config |
| `allow_inf_nan` | `False` | model_config |
| `use_enum_values` | `True` | model_config |

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `validate_stored_required_skills` | field | required_skill_levels | after | — |
| `validate_stored_reason_codes` | field | reason_codes | after | — |
| `strip_stored_assessment_text` | field | rationale, assessor | after | — |
| `reject_stored_nonfinite_confidence` | field | confidence | after | — |
| `validate_original_v1_band_and_review` | model | — | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `task_id` | `int` | `task_id` | Yes | No | — | ge=1 | — | — |
| `task_version` | `int` | `task_version` | Yes | No | — | ge=1 | — | — |
| `policy_version` | `Literal['model-aware-routing-v1']` | `policy_version` | No | No | `ROUTING_POLICY_VERSION` | — | — | — |
| `band` | `TaskDifficultyBand` | `band` | Yes | No | — | — | — | — |
| `axes` | `TaskDifficultyAxes` | `axes` | Yes | No | — | — | — | — |
| `required_skill_levels` | `dict[str, int]` | `required_skill_levels` | No | No | factory: `dict` | — | — | — |
| `required_model` | `RequiredModelEnvelope` | `required_model` | Yes | No | — | — | — | — |
| `review_mode` | `TaskReviewMode` | `review_mode` | Yes | No | — | — | — | — |
| `confidence` | `float` | `confidence` | Yes | No | — | ge=0.0; le=1.0 | — | — |
| `reason_codes` | `list[str]` | `reason_codes` | No | No | factory: `list` | — | — | — |
| `rationale` | `str` | `rationale` | Yes | No | — | min_length=1; max_length=unknown (MAX_ROUTING_TEXT_LENGTH) | — | — |
| `assessor` | `str` | `assessor` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `assessor_actor_id` | `int \| None` | `assessor_actor_id` | No | Yes | `None` | ge=1 | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `validate_stored_required_skills` | `(value: dict[str, int]) -> dict[str, int]` | `@field_validator('required_skill_levels')`, `@classmethod` | — |
| `validate_stored_reason_codes` | `(value: list[str]) -> list[str]` | `@field_validator('reason_codes')`, `@classmethod` | — |
| `strip_stored_assessment_text` | `(value: str) -> str` | `@field_validator('rationale', 'assessor')`, `@classmethod` | — |
| `reject_stored_nonfinite_confidence` | `(value: float) -> float` | `@field_validator('confidence')`, `@classmethod` | — |
| `validate_original_v1_band_and_review` | `() -> 'PersistedTaskRoutingAssessmentFields'` | `@model_validator(mode='after')` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["PersistedTaskRoutingAssessmentFields (backend/app/schemas/agent_routing.py)"]
    n1["BaseModel"]
    n2["TaskRoutingAssessmentResponse (backend/app/schemas/agent_routing.py)"]
    n3["PersistedTaskRoutingAssessmentFields.validate_original_v1_band_and_review (backend/app/schemas/agent_routing.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/agent_routing.md"
    click n2 "../modules/agent_routing.md"
    click n3 "../modules/agent_routing.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing](../modules/agent_routing.md) | 5 | `assessor`, `assessor_actor_id`, `axes`, `band`, `confidence`, `policy_version`, `rationale`, `reason_codes`, `required_model`, `required_skill_levels`, `review_mode`, `task_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
| Subclass | `TaskRoutingAssessmentResponse` | [agent_routing](../modules/agent_routing.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `PersistedTaskRoutingAssessmentFields.validate_original_v1_band_and_review` | type_reference | [agent_routing](../modules/agent_routing.md) | — |
