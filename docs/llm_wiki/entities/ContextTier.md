# ContextTier

**Location:** `backend/app/services/agent_routing_policy.py:109`
**Kind:** Enum
**Bases:** `StrEnum`
**Module:** [agent_routing_policy](../modules/agent_routing_policy.md)

## Description

Closed context-capacity tiers ordered by increasing capacity.

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `SMALL` | `'small'` | — |
| `MEDIUM` | `'medium'` | — |
| `LARGE` | `'large'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ContextTier (backend/app/services/agent_routing_policy.py)"]
    n1["StrEnum"]
    n2["backend/app/schemas/agent_routing.py"]
    n3["test_context_tier_ordering_matrix (backend/tests/test_agent_routing_contract.py)"]
    n4["test_every_context_tier_is_accepted (backend/tests/test_agent_routing_contract.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/agent_routing_policy.md"
    click n2 "../modules/agent_routing.md"
    click n3 "../modules/test_agent_routing_contract.md"
    click n4 "../modules/test_agent_routing_contract.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing_policy](../modules/agent_routing_policy.md) | 0 | `LARGE`, `MEDIUM`, `SMALL` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrEnum` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `agent_routing` | import | [agent_routing](../modules/agent_routing.md) | — |
| `test_context_tier_ordering_matrix` | type_reference | [test_agent_routing_contract](../modules/test_agent_routing_contract.md) | — |
| `test_every_context_tier_is_accepted` | type_reference | [test_agent_routing_contract](../modules/test_agent_routing_contract.md) | — |
