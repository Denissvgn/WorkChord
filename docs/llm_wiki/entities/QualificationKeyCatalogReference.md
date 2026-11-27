# QualificationKeyCatalogReference

**Location:** `backend/app/schemas/routing_qualification.py:124`
**Kind:** Pydantic model
**Bases:** `_RegistryModel`
**Module:** [schemas_routing_qualification](../modules/schemas_routing_qualification.md)

## Description

A catalog entry that holds the key.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `id` | `int` | `id` | Yes | No | — | — | — | — |
| `key` | `str` | `key` | Yes | No | — | — | — | — |
| `enabled` | `bool` | `enabled` | Yes | No | — | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["QualificationKeyCatalogReference (backend/app/schemas/routing_qualification.py)"]
    n1["_RegistryModel (backend/app/schemas/routing_qualification.py)"]
    n2["RoutingQualificationKeyService._bounded_usage (backend/app/services/routing_qualification_key_service.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_routing_qualification.md"
    click n1 "../modules/schemas_routing_qualification.md"
    click n2 "../modules/routing_qualification_key_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_routing_qualification](../modules/schemas_routing_qualification.md) | 0 | `enabled`, `id`, `key` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `_RegistryModel` | [schemas_routing_qualification](../modules/schemas_routing_qualification.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `RoutingQualificationKeyService._bounded_usage` | call | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | 1 |
