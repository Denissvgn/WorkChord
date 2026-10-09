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
| `app.models.delivery_dependency` | `DeliveryDependency`, `DeliveryDependency` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project`, `ProjectMilestone`, `Project`, `Project` |
| `app.models.recovery` | `TaskDeletionFence`, `TaskDeletionFence` |
| `app.models.system_settings` | `SystemSetting` |
| `app.models.task` | `Task` |
| `app.models.time_entry` | `TimeEntry`, `TimeEntry`, `TimeEntry` |
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
| `tests.migrations.test_project_identity` | `retained_entry` |
| `threading` | `Event`, `current_thread` |
| `typing` | `Any` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/database_migration/test_postgresql_transfer.py"]
    n1 --> n0
    click n1 "../modules/test_postgresql_transfer.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `backend` (16) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

> All 16 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_source_artifacts` | `(tmp_path: Path, configure_database, *, include_delivery_dependencies = False, include_retained_project_identity = False, include_deleted_task_allocation = False) -> tuple[Path, Path, str]` | — | — |
| `test_loader_rejects_concurrent_attempt_for_the_same_target` | `(tmp_path: Path, postgres_database, configure_database, monkeypatch: pytest.MonkeyPatch) -> None` | `@pytest.mark.postgresql`, `@pytest.mark.integration`, `@pytest.mark.allow_network` | — |
| `test_loader_is_idempotent_and_gate_opens_only_after_final_reconciliation` | `(tmp_path: Path, postgres_database, configure_database) -> None` | `@pytest.mark.postgresql`, `@pytest.mark.integration`, `@pytest.mark.allow_network` | — |
| `test_typed_delivery_targets_survive_source_transfer` | `(tmp_path, postgres_database, configure_database)` | `@pytest.mark.postgresql`, `@pytest.mark.integration`, `@pytest.mark.allow_network` | — |
| `test_transfer_preserves_deleted_project_allocation_progress_and_private_ledger` | `(tmp_path, postgres_database, configure_database)` | `@pytest.mark.postgresql`, `@pytest.mark.integration`, `@pytest.mark.allow_network` | — |
| `test_transfer_rejects_a_misrepresented_allocation_floor_before_target_writes` | `(tmp_path, postgres_database, configure_database)` | `@pytest.mark.postgresql`, `@pytest.mark.integration`, `@pytest.mark.allow_network` | — |
| `test_transfer_retains_deleted_task_allocation_and_private_recording_scope` | `(tmp_path, postgres_database, configure_database)` | `@pytest.mark.postgresql`, `@pytest.mark.integration`, `@pytest.mark.allow_network` | — |
