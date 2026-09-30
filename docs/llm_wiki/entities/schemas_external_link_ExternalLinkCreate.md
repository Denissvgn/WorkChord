# ExternalLinkCreate

**Location:** `backend/app/schemas/external_link.py:61`
**Kind:** Pydantic model
**Bases:** `ExternalLinkFields`
**Module:** [schemas_external_link](../modules/schemas_external_link.md)

## Description

Schema for creating a generic external link.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `entity_type` | `ExternalLinkEntityType` | `entity_type` | Yes | No | — | — | — | — |
| `entity_id` | `int` | `entity_id` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ExternalLinkCreate (backend/app/schemas/external_link.py)"]
    n1["ExternalLinkFields (backend/app/schemas/external_link.py)"]
    n2["backend/app/schemas/__init__.py"]
    n3["ExternalLinkService.create (backend/app/services/external_link_service.py)"]
    n4["ExternalLinkService.create_task_link (backend/app/services/external_link_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_external_link.md"
    click n1 "../modules/schemas_external_link.md"
    click n2 "../modules/schemas___init__.md"
    click n3 "../modules/external_link_service.md"
    click n4 "../modules/external_link_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_external_link](../modules/schemas_external_link.md) | 0 | `entity_id`, `entity_type` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ExternalLinkFields` | [schemas_external_link](../modules/schemas_external_link.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `ExternalLinkService.create` | type_reference | [external_link_service](../modules/external_link_service.md) | — |
| `ExternalLinkService.create_task_link` | call | [external_link_service](../modules/external_link_service.md) | 1 |
| `ExternalLinkService.create_task_link` | type_reference | [external_link_service](../modules/external_link_service.md) | — |
