# test_project_identity_scope Module

**Path:** `backend/tests/database_migration/test_project_identity_scope.py`

## Description

Ambiguous legacy identities stop before writes and never expose private records.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database_migration.project_identity` | `ProjectIdentityError`, `inspect_project_identity` |
| `app.database_migration.source` | `MigrationDataError`, `preflight_source` |
| `app.models.identity` | `CommandAudit` |
| `app.models.project` | `Project` |
| `app.models.time_entry` | `TimeEntry`, `TimeEntryRevision` |
| `app.services.upgrade_service` | `UpgradeError`, `run_alembic_upgrade` |
| `datetime` | `UTC`, `datetime` |
| `json` | `json` |
| `pytest` | `pytest` |
| `sqlalchemy` | `event` |
| `sqlalchemy.engine` | `Engine` |
| `tests.database_migration.test_source_preflight` | `_drain_evidence` |
| `tests.migrations.test_project_identity` | `legacy_store`, `retained_entry`, `seed_dependents` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database_migration/project_identity.py"]
    n1["backend/app/database_migration/source.py"]
    n2["backend/app/models/identity.py"]
    n3["backend/app/models/project.py"]
    n4["backend/app/models/time_entry.py"]
    n5["backend/app/services/upgrade_service.py"]
    n6["backend/tests/database_migration/test_project_identity_scope.py"]
    n7["backend/tests/database_migration/test_source_preflight.py"]
    n8["backend/tests/migrations/test_project_identity.py"]
    n1 --> n0
    n1 --> n5
    n5 --> n0
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n6 --> n5
    n6 --> n7
    n6 --> n8
    n7 --> n1
    n7 --> n5
    n8 --> n2
    n8 --> n3
    n8 --> n4
    n8 --> n5
    click n0 "../modules/project_identity.md"
    click n1 "../modules/source.md"
    click n2 "../modules/models_identity.md"
    click n3 "../modules/models_project.md"
    click n4 "../modules/models_time_entry.md"
    click n5 "../modules/upgrade_service.md"
    click n6 "../modules/test_project_identity_scope.md"
    click n7 "../modules/test_source_preflight.md"
    click n8 "../modules/test_project_identity.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [project_identity](../modules/project_identity.md) |
| Outbound | [source](../modules/source.md) |
| Outbound | [models_identity](../modules/models_identity.md) |
| Outbound | [models_project](../modules/models_project.md) |
| Outbound | [models_time_entry](../modules/models_time_entry.md) |
| Outbound | [upgrade_service](../modules/upgrade_service.md) |
| Outbound | [test_source_preflight](../modules/test_source_preflight.md) |
| Outbound | [test_project_identity](../modules/test_project_identity.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_ambiguous_retained_scope_blocks_upgrade_and_snapshot_before_writes` | `(tmp_path, configure_database, name)` | `@pytest.mark.sqlite`, `@pytest.mark.parametrize('name', ['Same display name', 'Different display name'])` | — |
| `test_collision_diagnostics_are_bounded_and_do_not_include_notes` | `(tmp_path, configure_database)` | `@pytest.mark.sqlite` | — |
| `test_incomplete_history_scan_fails_closed_without_mutation` | `(tmp_path, configure_database)` | `@pytest.mark.sqlite` | — |
