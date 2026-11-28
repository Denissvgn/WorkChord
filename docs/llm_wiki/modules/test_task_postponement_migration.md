# test_task_postponement_migration Module

**Path:** `backend/tests/migrations/test_task_postponement_migration.py`

## Description

Task postponement migrates a populated database unchanged, and never loses postponed work on rollback.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `command` |
| `app.models.agent` | `AgentActor`, `AgentRun`, `AgentTaskAssignment` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task`, `TaskDependency` |
| `app.models.task_postponement` | `TaskPostponement`, `TaskReactivationRequirement` |
| `app.models.task_status_log` | `TaskStatusLog` |
| `app.services.upgrade_service` | `alembic_config` |
| `datetime` | `date`, `datetime`, `timezone` |
| `pytest` | `pytest` |
| `sqlalchemy` | `create_engine`, `event`, `inspect`, `select` |
| `sqlalchemy.exc` | `IntegrityError` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/agent.py"]
    n1["backend/app/models/project.py"]
    n2["backend/app/models/task.py"]
    n3["backend/app/models/task_postponement.py"]
    n4["backend/app/models/task_status_log.py"]
    n5["backend/app/services/upgrade_service.py"]
    n6["backend/tests/migrations/test_task_postponement_migration.py"]
    n0 --> n1
    n0 --> n2
    n1 --> n0
    n1 --> n2
    n2 --> n0
    n2 --> n1
    n2 --> n4
    n4 --> n2
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n6 --> n5
    click n0 "../modules/models_agent.md"
    click n1 "../modules/models_project.md"
    click n2 "../modules/models_task.md"
    click n3 "../modules/models_task_postponement.md"
    click n4 "../modules/task_status_log.md"
    click n5 "../modules/upgrade_service.md"
    click n6 "../modules/test_task_postponement_migration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_project](../modules/models_project.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [models_task_postponement](../modules/models_task_postponement.md) |
| Outbound | [task_status_log](../modules/task_status_log.md) |
| Outbound | [upgrade_service](../modules/upgrade_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_populate` | `(db)` | — | Tasks in every prior status, with dependencies, history and agent execution. |
| `_rows` | `(db)` | — | — |
| `test_postponement_migration_upgrades_populated_data_and_refuses_losing_postponed_work` | `(dialect, request, tmp_path, configure_database)` | `@pytest.mark.parametrize('dialect', [pytest.param('sqlite', marks=pytest.mark.sqlite), pytest.param('postgresql', marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network])])` | — |
