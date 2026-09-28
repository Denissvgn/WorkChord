# ExplainScheduleRequest

**Location:** `backend/app/schemas/llm.py:103`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_llm](../modules/schemas_llm.md)

## Description

Request for schedule explanation.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `detail_level` | `str` | `detail_level` | No | No | `'full'` | pattern='^(brief\|full)$' | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ExplainScheduleRequest (backend/app/schemas/llm.py)"]
    n1["BaseModel"]
    n2["explain_schedule (backend/app/routers/llm.py)"]
    n3["backend/app/schemas/__init__.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_llm.md"
    click n2 "../modules/routers_llm.md"
    click n3 "../modules/schemas___init__.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_llm](../modules/schemas_llm.md) | 0 | `detail_level` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `explain_schedule` | call | [routers_llm](../modules/routers_llm.md) | 1 |
| `explain_schedule` | type_reference | [routers_llm](../modules/routers_llm.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
