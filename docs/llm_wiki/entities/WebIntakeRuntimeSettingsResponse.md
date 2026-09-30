# WebIntakeRuntimeSettingsResponse

**Location:** `backend/app/schemas/system_settings.py:74`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_system_settings](../modules/schemas_system_settings.md)

## Description

Resolved controlled web-intake runtime settings.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `rate_limit_per_minute` | `int` | `rate_limit_per_minute` | Yes | No | — | — | — | — |
| `has_token` | `bool` | `has_token` | Yes | No | — | — | — | — |
| `field_sources` | `dict[str, RuntimeSettingSource]` | `field_sources` | No | No | factory: `dict` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WebIntakeRuntimeSettingsResponse (backend/app/schemas/system_settings.py)"]
    n1["BaseModel"]
    n2["update_web_intake_settings (backend/app/routers/system_settings.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["RuntimeSettingsService.update_web_intake (backend/app/services/system_settings_service.py)"]
    n5["RuntimeSettingsService.web_intake_response (backend/app/services/system_settings_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/schemas_system_settings.md"
    click n2 "../modules/routers_system_settings.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/system_settings_service.md"
    click n5 "../modules/system_settings_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_system_settings](../modules/schemas_system_settings.md) | 0 | `field_sources`, `has_token`, `rate_limit_per_minute` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `update_web_intake_settings` | type_reference | [routers_system_settings](../modules/routers_system_settings.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `RuntimeSettingsService.update_web_intake` | type_reference | [system_settings_service](../modules/system_settings_service.md) | — |
| `RuntimeSettingsService.web_intake_response` | call | [system_settings_service](../modules/system_settings_service.md) | 1 |
| `RuntimeSettingsService.web_intake_response` | type_reference | [system_settings_service](../modules/system_settings_service.md) | — |
