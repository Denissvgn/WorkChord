# DifficultyAxis

**Location:** `backend/app/services/agent_routing_policy.py:133`
**Kind:** Enum
**Bases:** `StrEnum`
**Module:** [agent_routing_policy](../modules/agent_routing_policy.md)

## Description

The five governed task-difficulty axes.

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `REASONING` | `'reasoning'` | — |
| `AMBIGUITY` | `'ambiguity'` | — |
| `CONTEXT_BREADTH` | `'context_breadth'` | — |
| `RISK` | `'risk'` | — |
| `VERIFICATION_BURDEN` | `'verification_burden'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["DifficultyAxis (backend/app/services/agent_routing_policy.py)"]
    n1["StrEnum"]
    n2["backend/tests/test_agent_routing_contract.py"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/agent_routing_policy.md"
    click n2 "../modules/test_agent_routing_contract.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing_policy](../modules/agent_routing_policy.md) | 0 | `AMBIGUITY`, `CONTEXT_BREADTH`, `REASONING`, `RISK`, `VERIFICATION_BURDEN` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrEnum` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `test_agent_routing_contract` | import | [test_agent_routing_contract](../modules/test_agent_routing_contract.md) | — |
