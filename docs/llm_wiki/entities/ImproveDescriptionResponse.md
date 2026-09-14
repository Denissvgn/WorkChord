# ImproveDescriptionResponse

**Location:** `backend/app/schemas/llm.py:40`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_llm](../modules/schemas_llm.md)

## Description

Response from description improvement.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `improved_description` | `str` | `improved_description` | Yes | No | — | — | — | — |
| `language` | `str` | `language` | No | No | `'en'` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ImproveDescriptionResponse (backend/app/schemas/llm.py)"]
    n1["BaseModel"]
    n2["improve_task_description (backend/app/routers/llm.py)"]
    n3["improve_task_description_draft (backend/app/routers/llm.py)"]
    n4["backend/app/schemas/__init__.py"]
    n5["LLMService.improve_description (backend/app/services/llm_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/schemas_llm.md"
    click n2 "../modules/routers_llm.md"
    click n3 "../modules/routers_llm.md"
    click n4 "../modules/schemas___init__.md"
    click n5 "../modules/llm_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_llm](../modules/schemas_llm.md) | 0 | `improved_description`, `language` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `improve_task_description` | type_reference | [routers_llm](../modules/routers_llm.md) | — |
| `improve_task_description_draft` | type_reference | [routers_llm](../modules/routers_llm.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `LLMService.improve_description` | call | [llm_service](../modules/llm_service.md) | 3 |
| `LLMService.improve_description` | type_reference | [llm_service](../modules/llm_service.md) | — |
