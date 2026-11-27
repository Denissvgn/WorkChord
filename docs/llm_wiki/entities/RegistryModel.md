# _RegistryModel

**Location:** `backend/app/schemas/routing_qualification.py:25`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_routing_qualification](../modules/schemas_routing_qualification.md)

## Description

Shared base for the qualification key registry schemas. It forbids unknown fields and reads from ORM rows.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |
| `from_attributes` | `True` | model_config |

## Attributes

*No annotated attributes found.*

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["_RegistryModel (backend/app/schemas/routing_qualification.py)"]
    n1["BaseModel"]
    n2["QualificationKeyCalibrationReference (backend/app/schemas/routing_qualification.py)"]
    n3["QualificationKeyCatalogReference (backend/app/schemas/routing_qualification.py)"]
    n4["RoutingQualificationKeyDeclare (backend/app/schemas/routing_qualification.py)"]
    n5["RoutingQualificationKeyRegistryResponse (backend/app/schemas/routing_qualification.py)"]
    n6["RoutingQualificationKeyResponse (backend/app/schemas/routing_qualification.py)"]
    n7["RoutingQualificationKeyRetire (backend/app/schemas/routing_qualification.py)"]
    n8["RoutingQualificationKeyRevise (backend/app/schemas/routing_qualification.py)"]
    n9["RoutingQualificationKeyRevisionResponse (backend/app/schemas/routing_qualification.py)"]
    n10["RoutingQualificationKeyUsage (backend/app/schemas/routing_qualification.py)"]
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
    click n0 "../modules/schemas_routing_qualification.md"
    click n2 "../modules/schemas_routing_qualification.md"
    click n3 "../modules/schemas_routing_qualification.md"
    click n4 "../modules/schemas_routing_qualification.md"
    click n5 "../modules/schemas_routing_qualification.md"
    click n6 "../modules/schemas_routing_qualification.md"
    click n7 "../modules/schemas_routing_qualification.md"
    click n8 "../modules/schemas_routing_qualification.md"
    click n9 "../modules/schemas_routing_qualification.md"
    click n10 "../modules/schemas_routing_qualification.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_routing_qualification](../modules/schemas_routing_qualification.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
| Subclass | `QualificationKeyCalibrationReference` | [schemas_routing_qualification](../modules/schemas_routing_qualification.md) |
| Subclass | `QualificationKeyCatalogReference` | [schemas_routing_qualification](../modules/schemas_routing_qualification.md) |
| Subclass | `RoutingQualificationKeyDeclare` | [schemas_routing_qualification](../modules/schemas_routing_qualification.md) |
| Subclass | `RoutingQualificationKeyRegistryResponse` | [schemas_routing_qualification](../modules/schemas_routing_qualification.md) |
| Subclass | `RoutingQualificationKeyResponse` | [schemas_routing_qualification](../modules/schemas_routing_qualification.md) |
| Subclass | `RoutingQualificationKeyRetire` | [schemas_routing_qualification](../modules/schemas_routing_qualification.md) |
| Subclass | `RoutingQualificationKeyRevise` | [schemas_routing_qualification](../modules/schemas_routing_qualification.md) |
| Subclass | `RoutingQualificationKeyRevisionResponse` | [schemas_routing_qualification](../modules/schemas_routing_qualification.md) |
| Subclass | `RoutingQualificationKeyUsage` | [schemas_routing_qualification](../modules/schemas_routing_qualification.md) |
