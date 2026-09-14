# DatabaseConfigurationError

**Location:** `backend/app/database_config.py:39`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [database_config](../modules/database_config.md)

## Description

Raised when database settings are unsupported or unsafe.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["DatabaseConfigurationError (backend/app/database_config.py)"]
    n1["ValueError"]
    n2["_certificate_path (backend/app/database_config.py)"]
    n3["_settings_value (backend/app/database_config.py)"]
    n4["parse_database_configuration (backend/app/database_config.py)"]
    n5["backend/tests/database/test_database_configuration.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/database_config.md"
    click n2 "../modules/database_config.md"
    click n3 "../modules/database_config.md"
    click n4 "../modules/database_config.md"
    click n5 "../modules/test_database_configuration.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [database_config](../modules/database_config.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ValueError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_certificate_path` | call | [database_config](../modules/database_config.md) | 2 |
| `_settings_value` | call | [database_config](../modules/database_config.md) | 1 |
| `parse_database_configuration` | call | [database_config](../modules/database_config.md) | 20 |
| `test_database_configuration` | import | [test_database_configuration](../modules/test_database_configuration.md) | — |
