# RoutingContractModel

**Location:** `backend/app/schemas/agent_routing.py:204`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [agent_routing](../modules/agent_routing.md)

## Description

Strict deterministic base for data crossing a routing boundary.

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
| `validate_encoded_packet_size` | model | — | after | — |

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `validate_encoded_packet_size` | `() -> 'RoutingContractModel'` | `@model_validator(mode='after')` | — |
| `canonical_json_bytes` | `() -> bytes` | — | Return byte-stable normalized JSON for digests and parity checks. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RoutingContractModel (backend/app/schemas/agent_routing.py)"]
    n1["BaseModel"]
    n2["AgentModelBindingDisable (backend/app/schemas/agent_routing.py)"]
    n3["AgentModelBindingFields (backend/app/schemas/agent_routing.py)"]
    n4["AgentModelBindingUpdate (backend/app/schemas/agent_routing.py)"]
    n5["AgentModelCatalogDisable (backend/app/schemas/agent_routing.py)"]
    n6["AgentModelCatalogFields (backend/app/schemas/agent_routing.py)"]
    n7["AgentModelCatalogUpdate (backend/app/schemas/agent_routing.py)"]
    n8["AgentModelMutationReceipt (backend/app/schemas/agent_routing.py)"]
    n9["AgentRoutingCandidate (backend/app/schemas/agent_routing.py)"]
    n10["AgentRoutingExclusion (backend/app/schemas/agent_routing.py)"]
    n11["AgentRoutingPreviewCreate (backend/app/schemas/agent_routing.py)"]
    n12["AgentRoutingPreviewResponse (backend/app/schemas/agent_routing.py)"]
    n13["RequiredModelEnvelope (backend/app/schemas/agent_routing.py)"]
    n14["RoutingContractModel.validate_encoded_packet_size (backend/app/schemas/agent_routing.py)"]
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
    n12 --> n0
    n13 --> n0
    n14 --> n0
    click n0 "../modules/agent_routing.md"
    click n2 "../modules/agent_routing.md"
    click n3 "../modules/agent_routing.md"
    click n4 "../modules/agent_routing.md"
    click n5 "../modules/agent_routing.md"
    click n6 "../modules/agent_routing.md"
    click n7 "../modules/agent_routing.md"
    click n8 "../modules/agent_routing.md"
    click n9 "../modules/agent_routing.md"
    click n10 "../modules/agent_routing.md"
    click n11 "../modules/agent_routing.md"
    click n12 "../modules/agent_routing.md"
    click n13 "../modules/agent_routing.md"
    click n14 "../modules/agent_routing.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing](../modules/agent_routing.md) | 2 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
| Subclass | `AgentModelBindingDisable` | [agent_routing](../modules/agent_routing.md) |
| Subclass | `AgentModelBindingFields` | [agent_routing](../modules/agent_routing.md) |
| Subclass | `AgentModelBindingUpdate` | [agent_routing](../modules/agent_routing.md) |
| Subclass | `AgentModelCatalogDisable` | [agent_routing](../modules/agent_routing.md) |
| Subclass | `AgentModelCatalogFields` | [agent_routing](../modules/agent_routing.md) |
| Subclass | `AgentModelCatalogUpdate` | [agent_routing](../modules/agent_routing.md) |
| Subclass | `AgentModelMutationReceipt` | [agent_routing](../modules/agent_routing.md) |
| Subclass | `AgentRoutingCandidate` | [agent_routing](../modules/agent_routing.md) |
| Subclass | `AgentRoutingExclusion` | [agent_routing](../modules/agent_routing.md) |
| Subclass | `AgentRoutingPreviewCreate` | [agent_routing](../modules/agent_routing.md) |
| Subclass | `AgentRoutingPreviewResponse` | [agent_routing](../modules/agent_routing.md) |
| Subclass | `RequiredModelEnvelope` | [agent_routing](../modules/agent_routing.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `RoutingContractModel.validate_encoded_packet_size` | type_reference | [agent_routing](../modules/agent_routing.md) | — |
