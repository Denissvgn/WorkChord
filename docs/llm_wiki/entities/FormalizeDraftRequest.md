# FormalizeDraftRequest

**Location:** `backend/app/schemas/llm.py:11`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_llm](../modules/schemas_llm.md)

## Description

Request for formalizing unsaved task form data.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `title` | `str` | `title` | Yes | No | — | min_length=1 | — | Current unsaved task title |
| `description` | `Optional[str]` | `description` | No | Yes | `None` | — | — | Current unsaved task description |
| `context` | `Optional[str]` | `context` | No | Yes | `None` | — | — | Optional project context |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["FormalizeDraftRequest (backend/app/schemas/llm.py)"]
    n1["BaseModel"]
    n2["formalize_task_draft (backend/app/routers/llm.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_llm.md"
    click n2 "../modules/routers_llm.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_llm](../modules/schemas_llm.md) | 0 | `context`, `description`, `title` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `formalize_task_draft` | type_reference | [routers_llm](../modules/routers_llm.md) | — |
