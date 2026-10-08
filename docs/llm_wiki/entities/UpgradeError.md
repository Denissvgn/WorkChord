# UpgradeError

**Location:** `backend/app/services/upgrade_service.py:34`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [upgrade_service](../modules/upgrade_service.md)

## Description

Raised when a database cannot be upgraded safely.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["UpgradeError (backend/app/services/upgrade_service.py)"]
    n1["RuntimeError"]
    n2["main (backend/app/cli/upgrade.py)"]
    n3["_backup_precondition (backend/app/services/upgrade_service.py)"]
    n4["_validate_managed_revision (backend/app/services/upgrade_service.py)"]
    n5["assert_database_current (backend/app/services/upgrade_service.py)"]
    n6["head_revision (backend/app/services/upgrade_service.py)"]
    n7["run_alembic_upgrade (backend/app/services/upgrade_service.py)"]
    n8["run_database_repairs (backend/app/services/upgrade_service.py)"]
    n9["backend/tests/migrations/test_initial_schema.py"]
    n10["backend/tests/migrations/test_postgresql_migrations.py"]
    n11["backend/tests/migrations/test_sqlite_migrations.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    click n0 "../modules/upgrade_service.md"
    click n2 "../modules/upgrade.md"
    click n3 "../modules/upgrade_service.md"
    click n4 "../modules/upgrade_service.md"
    click n5 "../modules/upgrade_service.md"
    click n6 "../modules/upgrade_service.md"
    click n7 "../modules/upgrade_service.md"
    click n8 "../modules/upgrade_service.md"
    click n9 "../modules/test_initial_schema.md"
    click n10 "../modules/test_postgresql_migrations.md"
    click n11 "../modules/test_sqlite_migrations.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [upgrade_service](../modules/upgrade_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `main` | call | [upgrade](../modules/upgrade.md) | 4 |
| `_backup_precondition` | call | [upgrade_service](../modules/upgrade_service.md) | 2 |
| `_validate_managed_revision` | call | [upgrade_service](../modules/upgrade_service.md) | 1 |
| `assert_database_current` | call | [upgrade_service](../modules/upgrade_service.md) | 1 |
| `head_revision` | call | [upgrade_service](../modules/upgrade_service.md) | 1 |
| `run_alembic_upgrade` | call | [upgrade_service](../modules/upgrade_service.md) | 4 |
| `run_database_repairs` | call | [upgrade_service](../modules/upgrade_service.md) | 1 |
| `test_initial_schema` | import | [test_initial_schema](../modules/test_initial_schema.md) | — |
| `test_postgresql_migrations` | import | [test_postgresql_migrations](../modules/test_postgresql_migrations.md) | — |
| `test_sqlite_migrations` | import | [test_sqlite_migrations](../modules/test_sqlite_migrations.md) | — |
