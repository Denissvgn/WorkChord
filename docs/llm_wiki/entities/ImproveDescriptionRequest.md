# ImproveDescriptionRequest

**Location:** `backend/app/schemas/llm.py:34`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_llm](../modules/schemas_llm.md)

## Description

Request for improving task description.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `current_description` | `str` | `current_description` | Yes | No | — | — | — | — |
| `context` | `Optional[str]` | `context` | No | Yes | `None` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ImproveDescriptionRequest (backend/app/schemas/llm.py)"]
    n1["BaseModel"]
    n2["improve_task_description (backend/app/routers/llm.py)"]
    n3["improve_task_description_draft (backend/app/routers/llm.py)"]
    n4["backend/app/schemas/__init__.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_llm.md"
    click n2 "../modules/routers_llm.md"
    click n3 "../modules/routers_llm.md"
    click n4 "../modules/schemas___init__.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_llm](../modules/schemas_llm.md) | 0 | `context`, `current_description` |

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
