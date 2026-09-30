# AppRuntimeSettingsUpdate

**Location:** `backend/app/schemas/system_settings.py:99`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_system_settings](../modules/schemas_system_settings.md)

## Description

Update request for app-wide runtime settings.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `ui_language` | `LanguageCode \| None` | `ui_language` | No | Yes | `None` | — | — | — |
| `ai_language_mode` | `AILanguageMode \| None` | `ai_language_mode` | No | Yes | `None` | — | — | — |
| `reset_fields` | `list[str]` | `reset_fields` | No | No | factory: `list` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AppRuntimeSettingsUpdate (backend/app/schemas/system_settings.py)"]
    n1["BaseModel"]
    n2["update_app_settings (backend/app/routers/system_settings.py)"]
    n3["backend/app/schemas/__init__.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_system_settings.md"
    click n2 "../modules/routers_system_settings.md"
    click n3 "../modules/schemas___init__.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_system_settings](../modules/schemas_system_settings.md) | 0 | `ai_language_mode`, `reset_fields`, `ui_language` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `update_app_settings` | type_reference | [routers_system_settings](../modules/routers_system_settings.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
