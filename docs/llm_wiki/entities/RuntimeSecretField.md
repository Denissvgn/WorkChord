# RuntimeSecretField

**Location:** `backend/app/schemas/system_settings.py:19`
**Kind:** Pydantic model
**Bases:** `RuntimeSettingField`
**Module:** [schemas_system_settings](../modules/schemas_system_settings.md)

## Description

Resolved secret metadata without exposing the secret.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `has_value` | `bool` | `has_value` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RuntimeSecretField (backend/app/schemas/system_settings.py)"]
    n1["RuntimeSettingField (backend/app/schemas/system_settings.py)"]
    n2["backend/app/schemas/__init__.py"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_system_settings.md"
    click n1 "../modules/schemas_system_settings.md"
    click n2 "../modules/schemas___init__.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_system_settings](../modules/schemas_system_settings.md) | 0 | `has_value` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeSettingField` | [schemas_system_settings](../modules/schemas_system_settings.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
