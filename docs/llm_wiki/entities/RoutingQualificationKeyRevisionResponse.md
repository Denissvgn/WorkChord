# RoutingQualificationKeyRevisionResponse

**Location:** `backend/app/schemas/routing_qualification.py:109`
**Kind:** Pydantic model
**Bases:** `_RegistryModel`
**Module:** [schemas_routing_qualification](../modules/schemas_routing_qualification.md)

## Description

One append-only change to a declared key, with its reason.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `revision` | `PositiveRevision` | `revision` | Yes | No | — | — | — | — |
| `action` | `QualificationKeyAction` | `action` | Yes | No | — | — | — | — |
| `state` | `QualificationKeyState` | `state` | Yes | No | — | — | — | — |
| `label` | `str` | `label` | Yes | No | — | — | — | — |
| `description` | `str \| None` | `description` | No | Yes | `None` | — | — | — |
| `reason` | `str` | `reason` | Yes | No | — | — | — | — |
| `actor_type` | `str` | `actor_type` | Yes | No | — | — | — | — |
| `actor_id` | `int \| None` | `actor_id` | No | Yes | `None` | — | — | — |
| `correlation_id` | `str \| None` | `correlation_id` | No | Yes | `None` | — | — | — |
| `created_at` | `datetime` | `created_at` | Yes | No | — | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RoutingQualificationKeyRevisionResponse (backend/app/schemas/routing_qualification.py)"]
    n1["_RegistryModel (backend/app/schemas/routing_qualification.py)"]
    n2["backend/app/services/routing_qualification_key_service.py"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_routing_qualification.md"
    click n1 "../modules/schemas_routing_qualification.md"
    click n2 "../modules/routing_qualification_key_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_routing_qualification](../modules/schemas_routing_qualification.md) | 0 | `action`, `actor_id`, `actor_type`, `correlation_id`, `created_at`, `description`, `label`, `reason`, `revision`, `state` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `_RegistryModel` | [schemas_routing_qualification](../modules/schemas_routing_qualification.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `routing_qualification_key_service` | import | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | — |
