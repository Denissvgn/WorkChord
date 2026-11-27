# RoutingQualificationKeyUsage

**Location:** `backend/app/schemas/routing_qualification.py:139`
**Kind:** Pydantic model
**Bases:** `_RegistryModel`
**Module:** [schemas_routing_qualification](../modules/schemas_routing_qualification.md)

## Description

Catalog entries, calibration contracts and tasks whose current routing assessment name the key.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `catalog_entries` | `list[QualificationKeyCatalogReference]` | `catalog_entries` | No | No | factory: `list` | max_length=unknown (MAX_QUALIFICATION_KEY_USAGE_ITEMS) | — | — |
| `task_ids` | `list[int]` | `task_ids` | No | No | factory: `list` | max_length=unknown (MAX_QUALIFICATION_KEY_USAGE_ITEMS) | — | — |
| `catalog_entries_omitted` | `int` | `catalog_entries_omitted` | No | No | `0` | ge=0 | — | — |
| `task_ids_omitted` | `int` | `task_ids_omitted` | No | No | `0` | ge=0 | — | — |
| `calibration_contracts` | `list[QualificationKeyCalibrationReference]` | `calibration_contracts` | No | No | factory: `list` | max_length=unknown (MAX_QUALIFICATION_KEY_USAGE_ITEMS) | — | — |
| `calibration_contracts_omitted` | `int` | `calibration_contracts_omitted` | No | No | `0` | ge=0 | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `in_use` | `() -> bool` | `@property` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RoutingQualificationKeyUsage (backend/app/schemas/routing_qualification.py)"]
    n1["_RegistryModel (backend/app/schemas/routing_qualification.py)"]
    n2["RoutingQualificationKeyService._bounded_usage (backend/app/services/routing_qualification_key_service.py)"]
    n3["RoutingQualificationKeyService._retire_usage (backend/app/services/routing_qualification_key_service.py)"]
    n4["RoutingQualificationKeyService.usage (backend/app/services/routing_qualification_key_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_routing_qualification.md"
    click n1 "../modules/schemas_routing_qualification.md"
    click n2 "../modules/routing_qualification_key_service.md"
    click n3 "../modules/routing_qualification_key_service.md"
    click n4 "../modules/routing_qualification_key_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_routing_qualification](../modules/schemas_routing_qualification.md) | 1 | `calibration_contracts`, `calibration_contracts_omitted`, `catalog_entries`, `catalog_entries_omitted`, `task_ids`, `task_ids_omitted` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `_RegistryModel` | [schemas_routing_qualification](../modules/schemas_routing_qualification.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `RoutingQualificationKeyService._bounded_usage` | call | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | 1 |
| `RoutingQualificationKeyService._bounded_usage` | type_reference | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | — |
| `RoutingQualificationKeyService._retire_usage` | type_reference | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | — |
| `RoutingQualificationKeyService.usage` | type_reference | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | — |
