# EmailSettings

**Location:** `backend/app/services/email_settings_service.py:26`
**Kind:** Class
**Bases:** —
**Module:** [email_settings_service](../modules/email_settings_service.md)

**Decorators:** `@dataclass`

## Description

Resolved email settings.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `enabled` | `bool` | `False` | — |
| `smtp_host` | `str` | `''` | — |
| `smtp_port` | `int` | `587` | — |
| `smtp_user` | `str` | `''` | — |
| `smtp_password` | `str` | `''` | — |
| `smtp_from_email` | `str` | `'notifications@workchord.local'` | — |
| `smtp_use_tls` | `bool` | `True` | — |
| `field_sources` | `dict[str, RuntimeSettingSource]` | `field(default_factory=dict)` | — |
| `password_configured` | `Optional[bool]` | `None` | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `has_password` | `() -> bool` | `@property` | Return whether an SMTP password is configured. |
| `is_configured` | `() -> bool` | `@property` | Return whether email can be attempted. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["EmailSettings (backend/app/services/email_settings_service.py)"]
    n1["EmailSettingsService.get_instance (backend/app/services/email_settings_service.py)"]
    n2["EmailSettingsService.get_settings (backend/app/services/email_settings_service.py)"]
    n3["EmailSettingsService.get_settings_sync (backend/app/services/email_settings_service.py)"]
    n4["EmailSettingsService.update_settings (backend/app/services/email_settings_service.py)"]
    n5["backend/tests/test_runtime_boundaries.py"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/email_settings_service.md"
    click n1 "../modules/email_settings_service.md"
    click n2 "../modules/email_settings_service.md"
    click n3 "../modules/email_settings_service.md"
    click n4 "../modules/email_settings_service.md"
    click n5 "../modules/test_runtime_boundaries.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [email_settings_service](../modules/email_settings_service.md) | 2 | `enabled`, `field_sources`, `password_configured`, `smtp_from_email`, `smtp_host`, `smtp_password`, `smtp_port`, `smtp_use_tls`, `smtp_user` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `EmailSettingsService.get_instance` | type_reference | [email_settings_service](../modules/email_settings_service.md) | — |
| `EmailSettingsService.get_settings` | call | [email_settings_service](../modules/email_settings_service.md) | 1 |
| `EmailSettingsService.get_settings` | type_reference | [email_settings_service](../modules/email_settings_service.md) | — |
| `EmailSettingsService.get_settings_sync` | call | [email_settings_service](../modules/email_settings_service.md) | 2 |
| `EmailSettingsService.get_settings_sync` | type_reference | [email_settings_service](../modules/email_settings_service.md) | — |
| `EmailSettingsService.update_settings` | call | [email_settings_service](../modules/email_settings_service.md) | 1 |
| `EmailSettingsService.update_settings` | type_reference | [email_settings_service](../modules/email_settings_service.md) | — |
| `test_runtime_boundaries` | import | [test_runtime_boundaries](../modules/test_runtime_boundaries.md) | — |
