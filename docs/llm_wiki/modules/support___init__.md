# __init__ Module

**Path:** `backend/tests/support/__init__.py`

## Description

Reusable test infrastructure for database and concurrency qualification.

## Imports

| Source | Symbols |
|--------|---------|
| `.database` | `PostgresTestDatabase`, `PostgresTestDatabaseManager`, `UnsafeDatabaseTarget`, `assert_safe_test_database_url` |
| `.factories` | `LegacySQLiteFactory`, `MappedModelFactory` |
| `.faults` | `AsyncBarrier`, `FailureInjector`, `FrozenClock` |
| `.schema` | `cross_dialect_schema_diff`, `schema_snapshot` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/tests/conftest.py"]
    n1["backend/tests/database/test_github_closure_concurrency.py"]
    n2["backend/tests/database/test_postgresql_concurrency.py"]
    n3["backend/tests/migrations/test_postgresql_migrations.py"]
    n4["backend/tests/migrations/test_project_identity.py"]
    n5["backend/tests/migrations/test_sqlite_migrations.py"]
    n6["backend/tests/support/__init__.py"]
    n7["backend/tests/support/database.py"]
    n8["backend/tests/support/factories.py"]
    n9["backend/tests/support/faults.py"]
    n10["backend/tests/support/schema.py"]
    n11["backend/tests/test_database_harness.py"]
    n0 --> n6
    n1 --> n6
    n2 --> n6
    n3 --> n6
    n4 --> n6
    n5 --> n6
    n6 --> n7
    n6 --> n8
    n6 --> n9
    n6 --> n10
    n11 --> n6
    n11 --> n7
    click n0 "../modules/conftest.md"
    click n1 "../modules/test_github_closure_concurrency.md"
    click n2 "../modules/test_postgresql_concurrency.md"
    click n3 "../modules/test_postgresql_migrations.md"
    click n4 "../modules/test_project_identity.md"
    click n5 "../modules/test_sqlite_migrations.md"
    click n6 "../modules/support___init__.md"
    click n7 "../modules/support_database.md"
    click n8 "../modules/factories.md"
    click n9 "../modules/faults.md"
    click n10 "../modules/schema.md"
    click n11 "../modules/test_database_harness.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [conftest](../modules/conftest.md) |
| Inbound | [test_github_closure_concurrency](../modules/test_github_closure_concurrency.md) |
| Inbound | [test_postgresql_concurrency](../modules/test_postgresql_concurrency.md) |
| Inbound | [test_postgresql_migrations](../modules/test_postgresql_migrations.md) |
| Inbound | [test_project_identity](../modules/test_project_identity.md) |
| Inbound | [test_sqlite_migrations](../modules/test_sqlite_migrations.md) |
| Inbound | [test_database_harness](../modules/test_database_harness.md) |
| Outbound | [support_database](../modules/support_database.md) |
| Outbound | [factories](../modules/factories.md) |
| Outbound | [faults](../modules/faults.md) |
| Outbound | [schema](../modules/schema.md) |
