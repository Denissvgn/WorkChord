# RuntimeSettingsError

**Location:** `backend/app/services/system_settings_service.py:38`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [system_settings_service](../modules/system_settings_service.md)

## Description

Raised when a runtime settings update is invalid.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RuntimeSettingsError (backend/app/services/system_settings_service.py)"]
    n1["ValueError"]
    n2["RuntimeSettingsEncryptionError (backend/app/services/system_settings_service.py)"]
    n3["backend/app/routers/email_settings.py"]
    n4["backend/app/routers/system_settings.py"]
    n5["backend/app/services/email_settings_service.py"]
    n6["RuntimeSettingsService._coerce (backend/app/services/system_settings_service.py)"]
    n7["RuntimeSettingsService._definition (backend/app/services/system_settings_service.py)"]
    n8["RuntimeSettingsService._field_key (backend/app/services/system_settings_service.py)"]
    n9["RuntimeSettingsService._reject_endpoint_change_without_secret_rotation (backend/app/services/system_settings_service.py)"]
    n10["RuntimeSettingsService._validate_smtp_host_for_egress (backend/app/services/system_settings_service.py)"]
    n11["RuntimeSettingsService.has_secret (backend/app/services/system_settings_service.py)"]
    n12["RuntimeSettingsService.set_secret (backend/app/services/system_settings_service.py)"]
    n13["RuntimeSettingsService.set_value (backend/app/services/system_settings_service.py)"]
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
    n12 --> n0
    n13 --> n0
    click n0 "../modules/system_settings_service.md"
    click n2 "../modules/system_settings_service.md"
    click n3 "../modules/routers_email_settings.md"
    click n4 "../modules/routers_system_settings.md"
    click n5 "../modules/email_settings_service.md"
    click n6 "../modules/system_settings_service.md"
    click n7 "../modules/system_settings_service.md"
    click n8 "../modules/system_settings_service.md"
    click n9 "../modules/system_settings_service.md"
    click n10 "../modules/system_settings_service.md"
    click n11 "../modules/system_settings_service.md"
    click n12 "../modules/system_settings_service.md"
    click n13 "../modules/system_settings_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [system_settings_service](../modules/system_settings_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ValueError` | — |
| Subclass | `RuntimeSettingsEncryptionError` | [system_settings_service](../modules/system_settings_service.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `email_settings` | import | [routers_email_settings](../modules/routers_email_settings.md) | — |
| `system_settings` | import | [routers_system_settings](../modules/routers_system_settings.md) | — |
| `email_settings_service` | import | [email_settings_service](../modules/email_settings_service.md) | — |
| `RuntimeSettingsService._coerce` | call | [system_settings_service](../modules/system_settings_service.md) | 14 |
| `RuntimeSettingsService._definition` | call | [system_settings_service](../modules/system_settings_service.md) | 1 |
| `RuntimeSettingsService._field_key` | call | [system_settings_service](../modules/system_settings_service.md) | 1 |
| `RuntimeSettingsService._reject_endpoint_change_without_secret_rotation` | call | [system_settings_service](../modules/system_settings_service.md) | 1 |
| `RuntimeSettingsService._validate_smtp_host_for_egress` | call | [system_settings_service](../modules/system_settings_service.md) | 1 |
| `RuntimeSettingsService.has_secret` | call | [system_settings_service](../modules/system_settings_service.md) | 1 |
| `RuntimeSettingsService.set_secret` | call | [system_settings_service](../modules/system_settings_service.md) | 2 |
| `RuntimeSettingsService.set_value` | call | [system_settings_service](../modules/system_settings_service.md) | 1 |
