# test_sqlite_migrations Module

**Path:** `backend/tests/migrations/test_sqlite_migrations.py`

## Description

SQLite side of the fresh schema and inspection migration matrix.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `app` | `models` |
| `app.database` | `Base` |
| `app.services.upgrade_service` | `UpgradeError`, `alembic_config`, `assert_database_current`, `bootstrap_database_schema`, `head_revision`, `inspect_database`, `run_alembic_upgrade` |
| `pathlib` | `Path` |
| `pytest` | `pytest` |
| `sqlalchemy` | `create_engine`, `inspect`, `text` |
| `sqlite3` | `sqlite3` |
| `tests.support` | `schema_snapshot` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/services/upgrade_service.py"]
    n3["backend/tests/migrations/test_sqlite_migrations.py"]
    n4["backend/tests/support/__init__.py"]
    n0 --> n2
    n2 --> n0
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/upgrade_service.md"
    click n3 "../modules/test_sqlite_migrations.md"
    click n4 "../modules/support___init__.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [models___init__](../modules/models___init__.md) |
| Outbound | [upgrade_service](../modules/upgrade_service.md) |
| Outbound | [support___init__](../modules/support___init__.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `sqlite_url` | `(path: Path) -> str` | — | — |
| `test_single_head_invariant` | `() -> None` | — | — |
| `test_schema_only_bootstrap_is_current_and_data_empty` | `(tmp_path: Path, configure_database) -> None` | `@pytest.mark.sqlite` | — |
| `test_live_schema_column_contract_matches_model_metadata` | `(tmp_path: Path, configure_database) -> None` | `@pytest.mark.sqlite` | — |
| `test_unknown_nonempty_schema_is_refused` | `(tmp_path: Path, configure_database) -> None` | `@pytest.mark.sqlite` | — |
| `test_unknown_alembic_revision_is_refused` | `(tmp_path: Path, configure_database) -> None` | `@pytest.mark.sqlite` | — |
| `test_startup_assertion_refuses_stale_schema_without_mutation` | `(tmp_path: Path, configure_database) -> None` | `@pytest.mark.sqlite` | — |
| `test_alembic_config_preserves_percent_encoded_values` | `(configure_database) -> None` | — | — |
