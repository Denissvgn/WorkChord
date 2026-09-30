# test_postgresql_transfer Module

**Path:** `backend/tests/database_migration/test_postgresql_transfer.py`

## Description

Real PostgreSQL loader and fail-closed reconciliation tests.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app.database_migration` | `transfer` |
| `app.database_migration.catalog` | `transfer_order`, `transfer_tables` |
| `app.database_migration.manifest` | `write_document` |
| `app.database_migration.source` | `preflight_source`, `MigrationDataError` |
| `app.database_migration.transfer` | `load_snapshot`, `reconcile_snapshot`, `target_identifier` |
| `app.models.agent` | `AgentActor` |
| `app.models.calendar` | `Calendar` |
| `app.models.iteration` | `Iteration` |
| `app.models.system_settings` | `SystemSetting` |
| `app.models.task` | `Task` |
| `app.models.user_session` | `UserSession` |
| `app.services.upgrade_service` | `bootstrap_database_schema`, `database_configuration` |
| `concurrent.futures` | `ThreadPoolExecutor` |
| `cryptography.fernet` | `Fernet` |
| `datetime` | `UTC`, `datetime` |
| `json` | `json` |
| `os` | `os` |
| `pathlib` | `Path` |
| `pytest` | `pytest` |
| `sqlalchemy` | `create_engine`, `func`, `select`, `text` |
| `sqlalchemy.engine` | `Connection` |
| `sqlalchemy.orm` | `Session` |
| `subprocess` | `subprocess` |
| `sys` | `sys` |
| `threading` | `Event`, `current_thread` |
| `typing` | `Any` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database_migration/catalog.py"]
    n1["backend/app/database_migration/manifest.py"]
    n2["backend/app/database_migration/source.py"]
    n3["backend/app/database_migration/transfer.py"]
    n4["backend/app/models/agent.py"]
    n5["backend/app/models/calendar.py"]
    n6["backend/app/models/iteration.py"]
    n7["backend/app/models/system_settings.py"]
    n8["backend/app/models/task.py"]
    n9["backend/app/models/user_session.py"]
    n10["backend/app/services/upgrade_service.py"]
    n11["backend/tests/database_migration/test_postgresql_transfer.py"]
    n2 --> n0
    n2 --> n1
    n2 --> n10
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n10
    n4 --> n8
    n5 --> n6
    n6 --> n5
    n6 --> n8
    n8 --> n4
    n8 --> n6
    n11 --> n0
    n11 --> n1
    n11 --> n2
    n11 --> n3
    n11 --> n4
    n11 --> n5
    n11 --> n6
    n11 --> n7
    n11 --> n8
    n11 --> n9
    n11 --> n10
    click n0 "../modules/catalog.md"
    click n1 "../modules/database_migration_manifest.md"
    click n2 "../modules/source.md"
    click n3 "../modules/transfer.md"
    click n4 "../modules/models_agent.md"
    click n5 "../modules/models_calendar.md"
    click n6 "../modules/models_iteration.md"
    click n7 "../modules/models_system_settings.md"
    click n8 "../modules/models_task.md"
    click n9 "../modules/user_session.md"
    click n10 "../modules/upgrade_service.md"
    click n11 "../modules/test_postgresql_transfer.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [catalog](../modules/catalog.md) |
| Outbound | [database_migration_manifest](../modules/database_migration_manifest.md) |
| Outbound | [source](../modules/source.md) |
| Outbound | [transfer](../modules/transfer.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_calendar](../modules/models_calendar.md) |
| Outbound | [models_iteration](../modules/models_iteration.md) |
| Outbound | [models_system_settings](../modules/models_system_settings.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [user_session](../modules/user_session.md) |
| Outbound | [upgrade_service](../modules/upgrade_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_source_artifacts` | `(tmp_path: Path, configure_database) -> tuple[Path, Path, str]` | — | — |
| `test_loader_rejects_concurrent_attempt_for_the_same_target` | `(tmp_path: Path, postgres_database, configure_database, monkeypatch: pytest.MonkeyPatch) -> None` | `@pytest.mark.postgresql`, `@pytest.mark.integration`, `@pytest.mark.allow_network` | — |
| `test_loader_is_idempotent_and_gate_opens_only_after_final_reconciliation` | `(tmp_path: Path, postgres_database, configure_database) -> None` | `@pytest.mark.postgresql`, `@pytest.mark.integration`, `@pytest.mark.allow_network` | — |
