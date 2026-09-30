# test_authority_migrations Module

**Path:** `backend/tests/test_authority_migrations.py`

## Description

Initial authority schema, constraints and empty transfer targets.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `command` |
| `app.database_migration.catalog` | `transfer_tables` |
| `app.services.upgrade_service` | `alembic_config` |
| `pytest` | `pytest` |
| `sqlalchemy` | `create_engine`, `event`, `inspect`, `select` |
| `sqlalchemy.engine` | `make_url` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database_migration/catalog.py"]
    n1["backend/app/services/upgrade_service.py"]
    n2["backend/tests/test_authority_migrations.py"]
    n3["backend/tests/test_task_domain_migrations.py"]
    n2 --> n0
    n2 --> n1
    n3 --> n2
    click n0 "../modules/catalog.md"
    click n1 "../modules/upgrade_service.md"
    click n2 "../modules/test_authority_migrations.md"
    click n3 "../modules/test_task_domain_migrations.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [test_task_domain_migrations](../modules/test_task_domain_migrations.md) |
| Outbound | [catalog](../modules/catalog.md) |
| Outbound | [upgrade_service](../modules/upgrade_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `initial_database` | `(request, tmp_path, configure_database)` | `@pytest.fixture(params=[pytest.param('sqlite', marks=pytest.mark.sqlite), pytest.param('postgresql', marks=[pytest.mark.postgresql, pytest.mark.allow_network])])` | — |
| `test_schema_only_target_remains_empty_for_catalogued_transfer` | `(initial_database)` | — | — |
| `test_new_foreign_keys_and_uniqueness_are_declared` | `(initial_database)` | — | — |
