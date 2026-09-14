# RestartRequiredSetting

**Location:** `backend/app/schemas/system_settings.py:107`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_system_settings](../modules/schemas_system_settings.md)

## Description

Read-only setting that remains environment/startup bound.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `key` | `str` | `key` | Yes | No | — | — | — | — |
| `description` | `str` | `description` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RestartRequiredSetting (backend/app/schemas/system_settings.py)"]
    n1["BaseModel"]
    n2["backend/app/schemas/__init__.py"]
    n3["backend/app/services/system_settings_service.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_system_settings.md"
    click n2 "../modules/schemas___init__.md"
    click n3 "../modules/system_settings_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_system_settings](../modules/schemas_system_settings.md) | 0 | `description`, `key` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `system_settings_service` | import | [system_settings_service](../modules/system_settings_service.md) | — |
