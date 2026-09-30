# email_settings_service Module

**Path:** `backend/app/services/email_settings_service.py`

## Description

Email settings service backed by runtime system settings.

## Imports

| Source | Symbols |
|--------|---------|
| `aiosmtplib` | `aiosmtplib` |
| `app.commands` | `commit_or_flush` |
| `app.config` | `get_settings` |
| `app.schemas.system_settings` | `RuntimeSettingSource` |
| `app.services.system_settings_service` | `RuntimeSettingsEncryptionError`, `RuntimeSettingsError`, `RuntimeSettingsService` |
| `app.utils.url_policy` | `URLPolicyError`, `validate_public_host` |
| `asyncio` | `asyncio` |
| `dataclasses` | `dataclass`, `field` |
| `email.mime.multipart` | `MIMEMultipart` |
| `email.mime.text` | `MIMEText` |
| `logging` | `logging` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `typing` | `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/commands.py"]
    n1["backend/app/config.py"]
    n2["backend/app/routers/email_settings.py"]
    n3["backend/app/schemas/system_settings.py"]
    n4["backend/app/services/email_settings_service.py"]
    n5["backend/app/services/notification_service.py"]
    n6["backend/app/services/outbound_webhook_service.py"]
    n7["backend/app/services/system_settings_service.py"]
    n8["backend/app/utils/url_policy.py"]
    n9["backend/tests/test_runtime_boundaries.py"]
    n2 --> n4
    n2 --> n7
    n4 --> n0
    n4 --> n1
    n4 --> n3
    n4 --> n7
    n4 --> n8
    n5 --> n0
    n5 --> n4
    n6 --> n0
    n6 --> n4
    n6 --> n5
    n6 --> n8
    n7 --> n0
    n7 --> n1
    n7 --> n3
    n7 --> n8
    n8 --> n1
    n9 --> n1
    n9 --> n4
    n9 --> n5
    click n0 "../modules/commands.md"
    click n1 "../modules/config.md"
    click n2 "../modules/routers_email_settings.md"
    click n3 "../modules/schemas_system_settings.md"
    click n4 "../modules/email_settings_service.md"
    click n5 "../modules/notification_service.md"
    click n6 "../modules/outbound_webhook_service.md"
    click n7 "../modules/system_settings_service.md"
    click n8 "../modules/url_policy.md"
    click n9 "../modules/test_runtime_boundaries.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [routers_email_settings](../modules/routers_email_settings.md) |
| Inbound | [notification_service](../modules/notification_service.md) |
| Inbound | [outbound_webhook_service](../modules/outbound_webhook_service.md) |
| Inbound | [test_runtime_boundaries](../modules/test_runtime_boundaries.md) |
| Outbound | [commands](../modules/commands.md) |
| Outbound | [config](../modules/config.md) |
| Outbound | [schemas_system_settings](../modules/schemas_system_settings.md) |
| Outbound | [system_settings_service](../modules/system_settings_service.md) |
| Outbound | [url_policy](../modules/url_policy.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [EmailSettings](../entities/email_settings_service_EmailSettings.md) | 28 | — | Resolved email settings. |
| [EmailSettingsService](../entities/EmailSettingsService.md) | 54 | — | Manage email settings through ``system_settings``. |
