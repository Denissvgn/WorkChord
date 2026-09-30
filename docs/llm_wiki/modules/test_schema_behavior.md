# test_schema_behavior Module

**Path:** `backend/tests/database/test_schema_behavior.py`

## Description

Dual-dialect Boolean/JSON/time/constraint/RETURNING behavior matrix.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.models.agent` | `AgentActor` |
| `app.models.saved_view` | `SavedView` |
| `app.models.system_settings` | `SystemSetting` |
| `app.models.user_session` | `UserSession` |
| `app.services.upgrade_service` | `bootstrap_database_schema` |
| `app.utils.time` | `utc_now` |
| `cryptography.fernet` | `Fernet` |
| `datetime` | `UTC`, `datetime` |
| `pathlib` | `Path` |
| `pytest` | `pytest` |
| `sqlalchemy` | `create_engine`, `event`, `insert`, `inspect`, `select` |
| `sqlalchemy.exc` | `IntegrityError` |
| `sqlalchemy.orm` | `Session` |
| `sqlalchemy.pool` | `NullPool` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/agent.py"]
    n1["backend/app/models/saved_view.py"]
    n2["backend/app/models/system_settings.py"]
    n3["backend/app/models/user_session.py"]
    n4["backend/app/services/upgrade_service.py"]
    n5["backend/app/utils/time.py"]
    n6["backend/tests/database/test_schema_behavior.py"]
    n0 --> n5
    n1 --> n3
    n1 --> n5
    n2 --> n5
    n3 --> n1
    n3 --> n5
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n6 --> n5
    click n0 "../modules/models_agent.md"
    click n1 "../modules/models_saved_view.md"
    click n2 "../modules/models_system_settings.md"
    click n3 "../modules/user_session.md"
    click n4 "../modules/upgrade_service.md"
    click n5 "../modules/time.md"
    click n6 "../modules/test_schema_behavior.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_saved_view](../modules/models_saved_view.md) |
| Outbound | [models_system_settings](../modules/models_system_settings.md) |
| Outbound | [user_session](../modules/user_session.md) |
| Outbound | [upgrade_service](../modules/upgrade_service.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `behavior_engine` | `(database_url: str, *, sqlite: bool)` | — | — |
| `exercise_schema_behavior` | `(engine) -> None` | — | — |
| `test_sqlite_schema_behavior_matrix` | `(tmp_path: Path, configure_database) -> None` | `@pytest.mark.sqlite` | — |
| `test_postgresql_schema_behavior_matrix` | `(postgres_database, configure_database) -> None` | `@pytest.mark.postgresql`, `@pytest.mark.integration`, `@pytest.mark.allow_network` | — |
