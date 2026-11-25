# test_delivery_target_branch_migration Module

**Path:** `backend/tests/migrations/test_delivery_target_branch_migration.py`

## Description

A delivery prerequisite's target branch migrates reversibly and is never dropped silently.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `command` |
| `app.models.delivery_dependency` | `DeliveryDependency` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.services.upgrade_service` | `alembic_config` |
| `pytest` | `pytest` |
| `sqlalchemy` | `create_engine`, `inspect`, `select` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/delivery_dependency.py"]
    n1["backend/app/models/project.py"]
    n2["backend/app/models/task.py"]
    n3["backend/app/services/upgrade_service.py"]
    n4["backend/tests/migrations/test_delivery_target_branch_migration.py"]
    n0 --> n1
    n0 --> n2
    n1 --> n2
    n2 --> n1
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    click n0 "../modules/delivery_dependency.md"
    click n1 "../modules/models_project.md"
    click n2 "../modules/models_task.md"
    click n3 "../modules/upgrade_service.md"
    click n4 "../modules/test_delivery_target_branch_migration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [delivery_dependency](../modules/delivery_dependency.md) |
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
| `test_target_branch_migration_keeps_edges_and_refuses_losing_a_branch` | `(dialect, request, tmp_path, configure_database)` | `@pytest.mark.parametrize('dialect', [pytest.param('sqlite', marks=pytest.mark.sqlite), pytest.param('postgresql', marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network])])` | — |
