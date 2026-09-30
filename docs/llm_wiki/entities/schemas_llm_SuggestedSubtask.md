# SuggestedSubtask

**Location:** `backend/app/schemas/llm.py:18`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_llm](../modules/schemas_llm.md)

## Description

Suggested subtask from LLM.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `title` | `str` | `title` | Yes | No | — | — | — | — |
| `effort_days` | `float` | `effort_days` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SuggestedSubtask (backend/app/schemas/llm.py)"]
    n1["BaseModel"]
    n2["LLMService.formalize_task (backend/app/services/llm_service.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_llm.md"
    click n2 "../modules/llm_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_llm](../modules/schemas_llm.md) | 0 | `effort_days`, `title` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `LLMService.formalize_task` | call | [llm_service](../modules/llm_service.md) | 1 |
