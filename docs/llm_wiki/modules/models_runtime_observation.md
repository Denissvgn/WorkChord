# runtime_observation Module

**Path:** `backend/app/models/runtime_observation.py`

## Description

Advisory observations of agent runtime sessions, reported by independent observers.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `datetime` |
| `sqlalchemy` | `CheckConstraint`, `ForeignKey`, `Index`, `Integer`, `String`, `UniqueConstraint`, `event` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/runtime_observation.py"]
    n3["backend/app/services/runtime_observation_service.py"]
    n4["backend/app/utils/time.py"]
    n5["backend/tests/test_runtime_observations.py"]
    n1 --> n2
    n2 --> n0
    n2 --> n4
    n3 --> n2
    n3 --> n4
    n5 --> n2
    n5 --> n4
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_runtime_observation.md"
    click n3 "../modules/runtime_observation_service.md"
    click n4 "../modules/time.md"
    click n5 "../modules/test_runtime_observations.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [runtime_observation_service](../modules/runtime_observation_service.md) |
| Inbound | [test_runtime_observations](../modules/test_runtime_observations.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [AgentRuntimeObservation](../entities/AgentRuntimeObservation.md) | 14 | `Base` | What an independent observer saw of an agent runtime session. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `immutable_observation` | `(*_args)` | — | — |
