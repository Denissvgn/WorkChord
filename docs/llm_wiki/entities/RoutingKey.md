# RoutingKey

**Location:** `backend/app/schemas/agent_routing.py:60`
**Kind:** Type alias
**Bases:** —
**Module:** [agent_routing](../modules/agent_routing.md)
**Target:** `Annotated[str, StringConstraints(strip_whitespace=True, to_lower=True, min_length=1, max_length=120, pattern='^[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?$')]`

## Description

_Auto-generated from `RoutingKey` in `backend/app/schemas/agent_routing.py`._

## Attributes

*See the alias definition for its member types.*

## Methods

*See the alias definition for callable and member types.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RoutingKey (backend/app/schemas/agent_routing.py)"]
    n1["backend/app/schemas/routing_calibration.py"]
    n2["backend/app/schemas/routing_qualification.py"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/agent_routing.md"
    click n1 "../modules/schemas_routing_calibration.md"
    click n2 "../modules/schemas_routing_qualification.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [agent_routing](../modules/agent_routing.md) | 0 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `routing_calibration` | import | [schemas_routing_calibration](../modules/schemas_routing_calibration.md) | — |
| `routing_qualification` | import | [schemas_routing_qualification](../modules/schemas_routing_qualification.md) | — |
