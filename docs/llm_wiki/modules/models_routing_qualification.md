# routing_qualification Module

**Path:** `backend/app/models/routing_qualification.py`

## Description

A deployment's declared qualification keys and their append-only revisions.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `datetime` |
| `sqlalchemy` | `CheckConstraint`, `ForeignKey`, `Index`, `Integer`, `String`, `Text`, `UniqueConstraint` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column`, `relationship` |
| `typing` | `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/routing_qualification.py"]
    n3["backend/app/services/routing_qualification_key_service.py"]
    n4["backend/app/utils/time.py"]
    n5["backend/tests/test_agent_routing_service.py"]
    n6["backend/tests/test_routing_qualification_keys.py"]
    n1 --> n2
    n2 --> n0
    n2 --> n4
    n3 --> n2
    n3 --> n4
    n5 --> n2
    n5 --> n3
    n6 --> n0
    n6 --> n2
    n6 --> n3
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_routing_qualification.md"
    click n3 "../modules/routing_qualification_key_service.md"
    click n4 "../modules/time.md"
    click n5 "../modules/test_agent_routing_service.md"
    click n6 "../modules/test_routing_qualification_keys.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [routing_qualification_key_service](../modules/routing_qualification_key_service.md) |
| Inbound | [test_agent_routing_service](../modules/test_agent_routing_service.md) |
| Inbound | [test_routing_qualification_keys](../modules/test_routing_qualification_keys.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [RoutingQualificationKey](../entities/models_routing_qualification_RoutingQualificationKey.md) | 16 | `Base` | One deployment-declared key that catalog entries and task requirements may name. |
| [RoutingQualificationKeyRevision](../entities/models_routing_qualification_RoutingQualificationKeyRevision.md) | 54 | `Base` | The state a key had after one declare, revise or retire command, and why. |
