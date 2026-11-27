# test_task_supersession_migration Module

**Path:** `backend/tests/migrations/test_task_supersession_migration.py`

## Description

Supersession dispositions migrate reversibly; existing replacements keep their basis and none is dropped silently.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `command` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.models.task_replacement` | `TaskReplacement` |
| `app.services.upgrade_service` | `alembic_config` |
| `datetime` | `datetime`, `timezone` |
| `importlib` | `importlib` |
| `pytest` | `pytest` |
| `sqlalchemy` | `create_engine`, `inspect`, `select`, `MetaData`, `Table` |
| `sqlalchemy.exc` | `IntegrityError` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/project.py"]
    n1["backend/app/models/task.py"]
    n2["backend/app/models/task_replacement.py"]
    n3["backend/app/services/upgrade_service.py"]
    n4["backend/tests/migrations/test_task_supersession_migration.py"]
    n0 --> n1
    n1 --> n0
    n2 --> n1
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    click n0 "../modules/models_project.md"
    click n1 "../modules/models_task.md"
    click n2 "../modules/models_task_replacement.md"
    click n3 "../modules/upgrade_service.md"
    click n4 "../modules/test_task_supersession_migration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [models_project](../modules/models_project.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [models_task_replacement](../modules/models_task_replacement.md) |
| Outbound | [upgrade_service](../modules/upgrade_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_supersession_migration_keeps_replacements_and_refuses_losing_supersessions` | `(dialect, request, tmp_path, configure_database)` | `@pytest.mark.parametrize('dialect', [pytest.param('sqlite', marks=pytest.mark.sqlite), pytest.param('postgresql', marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network])])` | — |
| `_legacy_insert` | `(db, values)` | — | Insert through the pre-upgrade table shape, which has no disposition column. |
