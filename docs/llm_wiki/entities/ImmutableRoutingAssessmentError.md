# ImmutableRoutingAssessmentError

**Location:** `backend/app/models/agent.py:838`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [models_agent](../modules/models_agent.md)

## Description

Raised when application code attempts to mutate append-only evidence.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ImmutableRoutingAssessmentError (backend/app/models/agent.py)"]
    n1["RuntimeError"]
    n2["backend/app/models/__init__.py"]
    n3["_reject_routing_assessment_mutation (backend/app/models/agent.py)"]
    n4["backend/tests/test_agent_routing_data.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/models_agent.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/models_agent.md"
    click n4 "../modules/test_agent_routing_data.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_agent](../modules/models_agent.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `_reject_routing_assessment_mutation` | call | [models_agent](../modules/models_agent.md) | 1 |
| `test_agent_routing_data` | import | [test_agent_routing_data](../modules/test_agent_routing_data.md) | — |
