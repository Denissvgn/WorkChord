# RoutingQualificationKeyResponse

**Location:** `backend/app/schemas/routing_qualification.py:95`
**Kind:** Pydantic model
**Bases:** `_RegistryModel`
**Module:** [schemas_routing_qualification](../modules/schemas_routing_qualification.md)

## Description

The current state of one declared key.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `id` | `int` | `id` | Yes | No | — | — | — | — |
| `key` | `str` | `key` | Yes | No | — | — | — | — |
| `label` | `str` | `label` | Yes | No | — | — | — | — |
| `description` | `str \| None` | `description` | No | Yes | `None` | — | — | — |
| `state` | `QualificationKeyState` | `state` | Yes | No | — | — | — | — |
| `revision` | `PositiveRevision` | `revision` | Yes | No | — | — | — | — |
| `created_at` | `datetime` | `created_at` | Yes | No | — | — | — | — |
| `updated_at` | `datetime` | `updated_at` | Yes | No | — | — | — | — |
| `retired_at` | `datetime \| None` | `retired_at` | No | Yes | `None` | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RoutingQualificationKeyResponse (backend/app/schemas/routing_qualification.py)"]
    n1["_RegistryModel (backend/app/schemas/routing_qualification.py)"]
    n2["RoutingQualificationKeyDetail (backend/app/schemas/routing_qualification.py)"]
    n3["RoutingQualificationKeyService._response (backend/app/services/routing_qualification_key_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_routing_qualification.md"
    click n1 "../modules/schemas_routing_qualification.md"
    click n2 "../modules/schemas_routing_qualification.md"
    click n3 "../modules/routing_qualification_key_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_routing_qualification](../modules/schemas_routing_qualification.md) | 0 | `created_at`, `description`, `id`, `key`, `label`, `retired_at`, `revision`, `state`, `updated_at` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `_RegistryModel` | [schemas_routing_qualification](../modules/schemas_routing_qualification.md) |
| Subclass | `RoutingQualificationKeyDetail` | [schemas_routing_qualification](../modules/schemas_routing_qualification.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `RoutingQualificationKeyService._response` | type_reference | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | — |
