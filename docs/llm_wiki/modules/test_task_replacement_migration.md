# test_task_replacement_migration Module

**Path:** `backend/tests/migrations/test_task_replacement_migration.py`

## Description

Clean-replacement dispositions migrate reversibly and an existing disposition is never dropped silently.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `command` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.services.upgrade_service` | `alembic_config` |
| `datetime` | `datetime`, `timezone` |
| `pytest` | `pytest` |
| `sqlalchemy` | `MetaData`, `Table`, `create_engine`, `inspect`, `select` |
| `sqlalchemy.exc` | `IntegrityError` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/project.py"]
    n1["backend/app/models/task.py"]
    n2["backend/app/services/upgrade_service.py"]
    n3["backend/tests/migrations/test_task_replacement_migration.py"]
    n0 --> n1
    n1 --> n0
    n3 --> n0
    n3 --> n1
    n3 --> n2
    click n0 "../modules/models_project.md"
    click n1 "../modules/models_task.md"
    click n2 "../modules/upgrade_service.md"
    click n3 "../modules/test_task_replacement_migration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [models_project](../modules/models_project.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [upgrade_service](../modules/upgrade_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_replacement_migration_keeps_tasks_and_refuses_losing_dispositions` | `(dialect, request, tmp_path, configure_database)` | `@pytest.mark.parametrize('dialect', [pytest.param('sqlite', marks=pytest.mark.sqlite), pytest.param('postgresql', marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network])])` | — |
