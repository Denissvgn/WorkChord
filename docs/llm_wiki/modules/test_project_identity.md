# test_project_identity Module

**Path:** `backend/tests/migrations/test_project_identity.py`

## Description

Project allocation floors, dependent preservation and transactional rebuilds.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `command` |
| `app.models.calendar` | `Calendar` |
| `app.models.identity` | `CommandAudit`, `Principal`, `ProjectMembership` |
| `app.models.iteration` | `Iteration` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.models.time_entry` | `TimeEntry`, `TimeEntryRevision` |
| `app.services.upgrade_service` | `alembic_config`, `run_alembic_upgrade` |
| `datetime` | `UTC`, `datetime` |
| `pytest` | `pytest` |
| `sqlalchemy` | `MetaData`, `Table`, `create_engine`, `event`, `text` |
| `sqlalchemy.engine` | `Engine` |
| `sqlite3` | `sqlite3` |
| `tests.support` | `schema_snapshot` |
| `uuid` | `uuid4` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/tests/migrations/test_project_identity.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/test_project_identity.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (4) |
| Outbound | `backend` (8) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 3 | 1 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `legacy_store` | `(tmp_path, configure_database)` | — | — |
| `insert_legacy_project` | `(db, **values)` | — | Insert through the reflected legacy table so newer ORM columns stay out. |
| `retained_entry` | `(db, project_id)` | — | — |
| `seed_dependents` | `(db)` | — | — |
| `database_rows` | `(engine)` | — | — |
| `test_upgrade_preserves_dependents_and_retained_allocation_floor` | `(tmp_path, configure_database, empty_projects)` | `@pytest.mark.sqlite`, `@pytest.mark.parametrize('empty_projects', [False, True])` | — |
| `test_failed_rebuild_rolls_back_schema_and_all_dependent_rows` | `(tmp_path, configure_database, failure_point)` | `@pytest.mark.sqlite`, `@pytest.mark.parametrize('failure_point', ['drop table projects', 'create index ix_projects_status'])` | — |
| `test_direct_upgrade_preserves_enabled_foreign_keys` | `(tmp_path, configure_database)` | `@pytest.mark.sqlite` | — |
| `test_direct_upgrade_refuses_to_commit_a_callers_pending_writes` | `(tmp_path, configure_database)` | `@pytest.mark.sqlite` | — |
