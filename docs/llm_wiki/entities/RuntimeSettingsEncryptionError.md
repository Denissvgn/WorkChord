# RuntimeSettingsEncryptionError

**Location:** `backend/app/services/system_settings_service.py:42`
**Kind:** Class
**Bases:** `RuntimeSettingsError`
**Module:** [system_settings_service](../modules/system_settings_service.md)

## Description

Raised when a secret cannot be encrypted or decrypted.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RuntimeSettingsEncryptionError (backend/app/services/system_settings_service.py)"]
    n1["RuntimeSettingsError (backend/app/services/system_settings_service.py)"]
    n2["backend/app/services/email_settings_service.py"]
    n3["RuntimeSettingsService._decrypt_secret (backend/app/services/system_settings_service.py)"]
    n4["RuntimeSettingsService._fernet (backend/app/services/system_settings_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/system_settings_service.md"
    click n1 "../modules/system_settings_service.md"
    click n2 "../modules/email_settings_service.md"
    click n3 "../modules/system_settings_service.md"
    click n4 "../modules/system_settings_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [system_settings_service](../modules/system_settings_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `RuntimeSettingsError` | [system_settings_service](../modules/system_settings_service.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `email_settings_service` | import | [email_settings_service](../modules/email_settings_service.md) | — |
| `RuntimeSettingsService._decrypt_secret` | call | [system_settings_service](../modules/system_settings_service.md) | 1 |
| `RuntimeSettingsService._fernet` | call | [system_settings_service](../modules/system_settings_service.md) | 2 |
