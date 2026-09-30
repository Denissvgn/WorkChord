# DeliveryDatabase

**Location:** `backend/app/routers/delivery_dependencies.py:14`
**Kind:** Type alias
**Bases:** —
**Module:** [delivery_dependencies](../modules/delivery_dependencies.md)
**Target:** `Annotated[AsyncSession, Depends(get_db, scope='function')]`

## Description

_Auto-generated from `DeliveryDatabase` in `backend/app/routers/delivery_dependencies.py`._

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["DeliveryDatabase (backend/app/routers/delivery_dependencies.py)"]
    n1["add_delivery_dependency (backend/app/routers/delivery_dependencies.py)"]
    n2["list_delivery_dependencies (backend/app/routers/delivery_dependencies.py)"]
    n3["remove_delivery_dependency (backend/app/routers/delivery_dependencies.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/delivery_dependencies.md"
    click n1 "../modules/delivery_dependencies.md"
    click n2 "../modules/delivery_dependencies.md"
    click n3 "../modules/delivery_dependencies.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [delivery_dependencies](../modules/delivery_dependencies.md) | 0 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `add_delivery_dependency` | type_reference | [delivery_dependencies](../modules/delivery_dependencies.md) | — |
| `list_delivery_dependencies` | type_reference | [delivery_dependencies](../modules/delivery_dependencies.md) | — |
| `remove_delivery_dependency` | type_reference | [delivery_dependencies](../modules/delivery_dependencies.md) | — |
