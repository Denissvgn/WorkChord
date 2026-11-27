# test_catalog_effort_migration Module

**Path:** `backend/tests/migrations/test_catalog_effort_migration.py`

## Description

Catalog effort upgrades a populated catalog to an explicit unknown value and is never dropped silently.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `command` |
| `alembic.script` | `ScriptDirectory` |
| `app.models.agent` | `AgentActor`, `AgentModelBinding` |
| `app.services.upgrade_service` | `alembic_config` |
| `pytest` | `pytest` |
| `sqlalchemy` | `create_engine`, `inspect`, `text` |
| `sqlalchemy.exc` | `IntegrityError` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/agent.py"]
    n1["backend/app/services/upgrade_service.py"]
    n2["backend/tests/migrations/test_catalog_effort_migration.py"]
    n2 --> n0
    n2 --> n1
    click n0 "../modules/models_agent.md"
    click n1 "../modules/upgrade_service.md"
    click n2 "../modules/test_catalog_effort_migration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [upgrade_service](../modules/upgrade_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_check_names` | `(db) -> set[str]` | — | — |
| `test_effort_upgrade_marks_existing_entries_unknown_and_refuses_losing_a_setting` | `(dialect, request, tmp_path, configure_database)` | `@pytest.mark.parametrize('dialect', [pytest.param('sqlite', marks=pytest.mark.sqlite), pytest.param('postgresql', marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network])])` | — |
