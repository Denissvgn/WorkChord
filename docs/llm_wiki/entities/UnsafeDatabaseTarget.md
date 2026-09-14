# UnsafeDatabaseTarget

**Location:** `backend/tests/support/database.py:27`
**Kind:** Class
**Bases:** `RuntimeError`
**Module:** [support_database](../modules/support_database.md)

## Description

Raised before a fixture could touch a non-test database target.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["UnsafeDatabaseTarget (backend/tests/support/database.py)"]
    n1["RuntimeError"]
    n2["backend/tests/support/__init__.py"]
    n3["assert_safe_test_database_url (backend/tests/support/database.py)"]
    n4["PostgresTestDatabaseManager.__init__ (backend/tests/support/database.py)"]
    n5["PostgresTestDatabaseManager._drop_name (backend/tests/support/database.py)"]
    n6["PostgresTestDatabaseManager.create (backend/tests/support/database.py)"]
    n7["PostgresTestDatabaseManager.drop (backend/tests/support/database.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/support_database.md"
    click n2 "../modules/support___init__.md"
    click n3 "../modules/support_database.md"
    click n4 "../modules/support_database.md"
    click n5 "../modules/support_database.md"
    click n6 "../modules/support_database.md"
    click n7 "../modules/support_database.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [support_database](../modules/support_database.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [support___init__](../modules/support___init__.md) | — |
| `assert_safe_test_database_url` | call | [support_database](../modules/support_database.md) | 6 |
| `PostgresTestDatabaseManager.__init__` | call | [support_database](../modules/support_database.md) | 5 |
| `PostgresTestDatabaseManager._drop_name` | call | [support_database](../modules/support_database.md) | 1 |
| `PostgresTestDatabaseManager.create` | call | [support_database](../modules/support_database.md) | 9 |
| `PostgresTestDatabaseManager.drop` | call | [support_database](../modules/support_database.md) | 1 |
