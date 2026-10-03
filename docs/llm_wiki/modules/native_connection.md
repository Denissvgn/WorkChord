# native_connection Module

**Path:** `backend/app/models/native_connection.py`

## Description

Short-lived browser consent for a proof-bound native session.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `datetime` |
| `sqlalchemy` | `ForeignKey`, `String` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/native_connection.py"]
    n3["backend/app/services/native_session_service.py"]
    n4["backend/app/utils/time.py"]
    n5["backend/tests/test_native_connections.py"]
    n1 --> n2
    n2 --> n0
    n2 --> n4
    n3 --> n2
    n3 --> n4
    n5 --> n2
    n5 --> n4
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/native_connection.md"
    click n3 "../modules/native_session_service.md"
    click n4 "../modules/time.md"
    click n5 "../modules/test_native_connections.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [native_session_service](../modules/native_session_service.md) |
| Inbound | [test_native_connections](../modules/test_native_connections.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [NativeConnection](../entities/NativeConnection.md) | 12 | `Base` | — |
