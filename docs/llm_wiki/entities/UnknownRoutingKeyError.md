# UnknownRoutingKeyError

**Location:** `backend/app/services/agent_routing_policy.py:492`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [agent_routing_policy](../modules/agent_routing_policy.md)

## Description

A key is neither a built-in routing skill key nor a declared qualification key.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(keys: Iterable[str])` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["UnknownRoutingKeyError (backend/app/services/agent_routing_policy.py)"]
    n1["ValueError"]
    n2["backend/app/routers/agent_planning.py"]
    n3["require_known_routing_keys (backend/app/services/agent_routing_policy.py)"]
    n4["backend/tests/test_agent_routing_service.py"]
    n5["backend/tests/test_routing_qualification_keys.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/agent_routing_policy.md"
    click n2 "../modules/routers_agent_planning.md"
    click n3 "../modules/agent_routing_policy.md"
    click n4 "../modules/test_agent_routing_service.md"
    click n5 "../modules/test_routing_qualification_keys.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing_policy](../modules/agent_routing_policy.md) | 1 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ValueError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `agent_planning` | import | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `require_known_routing_keys` | call | [agent_routing_policy](../modules/agent_routing_policy.md) | 1 |
| `test_agent_routing_service` | import | [test_agent_routing_service](../modules/test_agent_routing_service.md) | — |
| `test_routing_qualification_keys` | import | [test_routing_qualification_keys](../modules/test_routing_qualification_keys.md) | — |
