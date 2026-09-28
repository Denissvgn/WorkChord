# RoutingModelEnvelopeDecision

**Location:** `backend/app/services/agent_routing_policy.py:631`
**Kind:** Class
**Bases:** —
**Module:** [agent_routing_policy](../modules/agent_routing_policy.md)

**Decorators:** `@dataclass(frozen=True)`

## Description

Deterministic binding/catalog capability evidence for one candidate.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `hard_blocker_codes` | `tuple[str, ...]` | `()` | — |
| `adequacy_class` | `int \| None` | `None` | — |
| `missing_modality_tags` | `tuple[str, ...]` | `()` | — |
| `missing_tool_tags` | `tuple[str, ...]` | `()` | — |
| `missing_data_policy_tags` | `tuple[str, ...]` | `()` | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `eligible` | `() -> bool` | `@property` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RoutingModelEnvelopeDecision (backend/app/services/agent_routing_policy.py)"]
    n1["evaluate_model_envelope (backend/app/services/agent_routing_policy.py)"]
    n1 --> n0
    click n0 "../modules/agent_routing_policy.md"
    click n1 "../modules/agent_routing_policy.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing_policy](../modules/agent_routing_policy.md) | 1 | `adequacy_class`, `hard_blocker_codes`, `missing_data_policy_tags`, `missing_modality_tags`, `missing_tool_tags` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `evaluate_model_envelope` | call | [agent_routing_policy](../modules/agent_routing_policy.md) | 1 |
| `evaluate_model_envelope` | type_reference | [agent_routing_policy](../modules/agent_routing_policy.md) | — |
