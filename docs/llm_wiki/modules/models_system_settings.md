# system_settings Module

**Path:** `backend/app/models/system_settings.py`

## Description

Runtime system settings model.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `datetime` |
| `sqlalchemy` | `Boolean`, `Index`, `Integer`, `JSON`, `String`, `Text`, `UniqueConstraint` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column` |
| `typing` | `Any`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/system_settings.py"]
    n3["backend/app/services/system_settings_service.py"]
    n4["backend/app/utils/time.py"]
    n5["backend/tests/database/test_schema_behavior.py"]
    n6["backend/tests/database_migration/test_postgresql_transfer.py"]
    n1 --> n2
    n2 --> n0
    n2 --> n4
    n3 --> n2
    n5 --> n2
    n5 --> n4
    n6 --> n2
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_system_settings.md"
    click n3 "../modules/system_settings_service.md"
    click n4 "../modules/time.md"
    click n5 "../modules/test_schema_behavior.md"
    click n6 "../modules/test_postgresql_transfer.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [system_settings_service](../modules/system_settings_service.md) |
| Inbound | [test_schema_behavior](../modules/test_schema_behavior.md) |
| Inbound | [test_postgresql_transfer](../modules/test_postgresql_transfer.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [SystemSetting](../entities/SystemSetting.md) | 12 | `Base` | One catalogued runtime configuration value. |
