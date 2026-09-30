# DifficultyBand

**Location:** `backend/app/services/agent_routing_policy.py:143`
**Kind:** Enum
**Bases:** `StrEnum`
**Module:** [agent_routing_policy](../modules/agent_routing_policy.md)

## Description

Derived task-difficulty bands.

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `ROUTINE` | `'routine'` | — |
| `STANDARD` | `'standard'` | — |
| `ADVANCED` | `'advanced'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["DifficultyBand (backend/app/services/agent_routing_policy.py)"]
    n1["StrEnum"]
    n2["backend/app/schemas/agent_routing.py"]
    n3["backend/tests/test_agent_routing_contract.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/agent_routing_policy.md"
    click n2 "../modules/agent_routing.md"
    click n3 "../modules/test_agent_routing_contract.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing_policy](../modules/agent_routing_policy.md) | 0 | `ADVANCED`, `ROUTINE`, `STANDARD` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrEnum` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `agent_routing` | import | [agent_routing](../modules/agent_routing.md) | — |
| `test_agent_routing_contract` | import | [test_agent_routing_contract](../modules/test_agent_routing_contract.md) | — |
