# RoutingCandidateSummary

**Location:** `backend/app/schemas/agent_routing.py:1236`
**Kind:** Pydantic model
**Bases:** `RoutingContractModel`
**Module:** [agent_routing](../modules/agent_routing.md)

## Description

Compact ordered eligible-candidate evidence retained on assignment.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `actor_id` | `int` | `actor_id` | Yes | No | — | ge=1; strict=True | — | — |
| `profile_id` | `int` | `profile_id` | Yes | No | — | ge=1; strict=True | — | — |
| `model_binding_id` | `int` | `model_binding_id` | Yes | No | — | ge=1; strict=True | — | — |
| `model_binding_revision` | `PositiveRevision` | `model_binding_revision` | Yes | No | — | — | — | — |
| `model_catalog_key` | `RoutingKey` | `model_catalog_key` | Yes | No | — | — | — | — |
| `rank` | `int` | `rank` | Yes | No | — | ge=1; strict=True | — | — |
| `adequacy_class` | `int` | `adequacy_class` | Yes | No | — | ge=0; strict=True | — | — |
| `cost_tier` | `ModelCostTier` | `cost_tier` | Yes | No | — | — | — | — |
| `latency_tier` | `ModelLatencyTier` | `latency_tier` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RoutingCandidateSummary (backend/app/schemas/agent_routing.py)"]
    n1["RoutingContractModel (backend/app/schemas/agent_routing.py)"]
    n0 --> n1
    click n0 "../modules/agent_routing.md"
    click n1 "../modules/agent_routing.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing](../modules/agent_routing.md) | 0 | `actor_id`, `adequacy_class`, `cost_tier`, `latency_tier`, `model_binding_id`, `model_binding_revision`, `model_catalog_key`, `profile_id`, `rank` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RoutingContractModel` | [agent_routing](../modules/agent_routing.md) |
