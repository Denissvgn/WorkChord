# GroundedFact

**Location:** `backend/app/schemas/llm.py:46`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_llm](../modules/schemas_llm.md)

## Description

Fact or claim tied to an explicit source in the AI context pack.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `claim` | `str` | `claim` | Yes | No | — | min_length=1 | — | — |
| `source` | `str` | `source` | Yes | No | — | min_length=1 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GroundedFact (backend/app/schemas/llm.py)"]
    n1["BaseModel"]
    n2["backend/app/schemas/__init__.py"]
    n3["LLMService._grounded_facts_from_context (backend/app/services/llm_service.py)"]
    n4["LLMService._normalize_grounded_facts (backend/app/services/llm_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_llm.md"
    click n2 "../modules/schemas___init__.md"
    click n3 "../modules/llm_service.md"
    click n4 "../modules/llm_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_llm](../modules/schemas_llm.md) | 0 | `claim`, `source` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `LLMService._grounded_facts_from_context` | call | [llm_service](../modules/llm_service.md) | 4 |
| `LLMService._grounded_facts_from_context` | type_reference | [llm_service](../modules/llm_service.md) | — |
| `LLMService._normalize_grounded_facts` | call | [llm_service](../modules/llm_service.md) | 1 |
| `LLMService._normalize_grounded_facts` | type_reference | [llm_service](../modules/llm_service.md) | — |
