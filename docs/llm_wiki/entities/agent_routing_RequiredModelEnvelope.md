# RequiredModelEnvelope

**Location:** `backend/app/schemas/agent_routing.py:580`
**Kind:** Pydantic model
**Bases:** `RoutingContractModel`
**Module:** [agent_routing](../modules/agent_routing.md)

## Description

Minimum provider-neutral runtime capabilities required by a task.

The host-shell tool requirement still applies to execution when the PM permits source-only verification. The optional review setting is omitted from the serialized envelope unless selected so existing assessment receipts retain their original representation.

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `validate_qualification_keys` | field | qualification_keys | before | — |
| `require_integer_reasoning_tier` | field | minimum_reasoning_tier | before | — |
| `require_ranked_effort` | field | minimum_effort | after | — |
| `validate_tags` | field | modality_tags, tool_tags, data_policy_tags | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `minimum_reasoning_tier` | `ReasoningTier` | `minimum_reasoning_tier` | Yes | No | — | — | — | — |
| `minimum_context_tier` | `ModelContextTier` | `minimum_context_tier` | Yes | No | — | — | — | — |
| `minimum_effort` | `ModelEffortSetting \| None` | `minimum_effort` | No | Yes | `None` | — | — | Lowest effort setting a candidate model may run at; omitted when the task states no effort requirement. |
| `modality_tags` | `list[str]` | `modality_tags` | No | No | factory: `lambda: ['text']` | — | — | — |
| `tool_tags` | `list[str]` | `tool_tags` | No | No | factory: `list` | — | — | — |
| `allow_source_only_review` | `bool` | `allow_source_only_review` | No | No | `False` | strict=True | — | — |
| `data_policy_tags` | `list[str]` | `data_policy_tags` | No | No | factory: `list` | — | — | — |
| `qualification_keys` | `list[str]` | `qualification_keys` | No | No | factory: `list` | — | — | Built-in or declared qualification keys the candidate's catalog entry must hold; omitted when none are required. |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `validate_qualification_keys` | `(value: Any) -> Any` | `@field_validator('qualification_keys', mode='before')`, `@classmethod` | — |
| `require_integer_reasoning_tier` | `(value: Any) -> Any` | `@field_validator('minimum_reasoning_tier', mode='before')`, `@classmethod` | — |
| `require_ranked_effort` | `(value: ModelEffort \| None) -> ModelEffort \| None` | `@field_validator('minimum_effort')`, `@classmethod` | — |
| `validate_tags` | `(value: list[str], info: Any) -> list[str]` | `@field_validator('modality_tags', 'tool_tags', 'data_policy_tags')`, `@classmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RequiredModelEnvelope (backend/app/schemas/agent_routing.py)"]
    n1["RoutingContractModel (backend/app/schemas/agent_routing.py)"]
    n2["test_required_envelope_omits_empty_qualification_keys_from_its_stored_shape (backend/tests/test_routing_qualification_keys.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/agent_routing.md"
    click n1 "../modules/agent_routing.md"
    click n2 "../modules/test_routing_qualification_keys.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing](../modules/agent_routing.md) | 4 | `allow_source_only_review`, `data_policy_tags`, `minimum_context_tier`, `minimum_effort`, `minimum_reasoning_tier`, `modality_tags`, `qualification_keys`, `tool_tags` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RoutingContractModel` | [agent_routing](../modules/agent_routing.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `test_required_envelope_omits_empty_qualification_keys_from_its_stored_shape` | call | [test_routing_qualification_keys](../modules/test_routing_qualification_keys.md) | 3 |
