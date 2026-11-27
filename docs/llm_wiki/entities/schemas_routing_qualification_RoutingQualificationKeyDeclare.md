# RoutingQualificationKeyDeclare

**Location:** `backend/app/schemas/routing_qualification.py:40`
**Kind:** Pydantic model
**Bases:** `_RegistryModel`
**Module:** [schemas_routing_qualification](../modules/schemas_routing_qualification.md)

## Description

Declare a new key, or bring back a retired one under the same name.

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `normalize_key` | field | key | before | — |
| `strip_label` | field | label | after | — |
| `strip_description` | field | description | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `key` | `RoutingKey` | `key` | Yes | No | — | — | — | — |
| `label` | `str` | `label` | Yes | No | — | min_length=1; max_length=unknown (MAX_QUALIFICATION_KEY_LABEL) | — | — |
| `description` | `str \| None` | `description` | No | Yes | `None` | max_length=unknown (MAX_QUALIFICATION_KEY_DESCRIPTION) | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `normalize_key` | `(value: object) -> object` | `@field_validator('key', mode='before')`, `@classmethod` | — |
| `strip_label` | `(value: str) -> str` | `@field_validator('label')`, `@classmethod` | — |
| `strip_description` | `(value: str \| None) -> str \| None` | `@field_validator('description')`, `@classmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RoutingQualificationKeyDeclare (backend/app/schemas/routing_qualification.py)"]
    n1["_RegistryModel (backend/app/schemas/routing_qualification.py)"]
    n2["declare_routing_qualification_key (backend/app/routers/agent_catalog.py)"]
    n3["RoutingQualificationKeyService.declare (backend/app/services/routing_qualification_key_service.py)"]
    n4["test_a_project_scoped_agent_can_require_a_declared_key (backend/tests/test_agent_routing_service.py)"]
    n5["test_declared_qualification_key_is_a_requirement_the_candidate_must_hold (backend/tests/test_agent_routing_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/schemas_routing_qualification.md"
    click n1 "../modules/schemas_routing_qualification.md"
    click n2 "../modules/agent_catalog.md"
    click n3 "../modules/routing_qualification_key_service.md"
    click n4 "../modules/test_agent_routing_service.md"
    click n5 "../modules/test_agent_routing_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_routing_qualification](../modules/schemas_routing_qualification.md) | 3 | `description`, `key`, `label` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `_RegistryModel` | [schemas_routing_qualification](../modules/schemas_routing_qualification.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `declare_routing_qualification_key` | type_reference | [agent_catalog](../modules/agent_catalog.md) | — |
| `RoutingQualificationKeyService.declare` | type_reference | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) | — |
| `test_a_project_scoped_agent_can_require_a_declared_key` | call | [test_agent_routing_service](../modules/test_agent_routing_service.md) | 1 |
| `test_declared_qualification_key_is_a_requirement_the_candidate_must_hold` | call | [test_agent_routing_service](../modules/test_agent_routing_service.md) | 1 |
