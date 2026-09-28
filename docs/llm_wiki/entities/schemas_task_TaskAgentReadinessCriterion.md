# TaskAgentReadinessCriterion

**Location:** `backend/app/schemas/task.py:167`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task](../modules/schemas_task.md)

## Description

One deterministic criterion used for agent-readiness evaluation.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `key` | `str` | `key` | Yes | No | — | — | — | — |
| `label` | `str` | `label` | Yes | No | — | — | — | — |
| `passed` | `bool` | `passed` | Yes | No | — | — | — | — |
| `reason` | `str` | `reason` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskAgentReadinessCriterion (backend/app/schemas/task.py)"]
    n1["BaseModel"]
    n2["backend/app/schemas/__init__.py"]
    n3["_add_criterion (backend/app/services/agent_readiness.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_task.md"
    click n2 "../modules/schemas___init__.md"
    click n3 "../modules/agent_readiness.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task](../modules/schemas_task.md) | 0 | `key`, `label`, `passed`, `reason` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `_add_criterion` | call | [agent_readiness](../modules/agent_readiness.md) | 1 |
| `_add_criterion` | type_reference | [agent_readiness](../modules/agent_readiness.md) | — |
