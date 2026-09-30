# system_settings_service Module

**Path:** `backend/app/services/system_settings_service.py`

## Description

DB-backed runtime system settings resolution.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `commit_or_flush` |
| `app.config` | `get_settings` |
| `app.models.system_settings` | `SystemSetting` |
| `app.schemas.system_settings` | `AppRuntimeSettingsResponse`, `GitHubRuntimeSettingsResponse`, `LLMRuntimeSettingsResponse`, `RestartRequiredSetting`, `SystemSettingsResponse`, `WebIntakeRuntimeSettingsResponse` |
| `app.utils.url_policy` | `URLPolicyError`, `normalize_provider_api_url`, `validate_public_host` |
| `cryptography.fernet` | `Fernet` |
| `dataclasses` | `dataclass` |
| `json` | `json` |
| `logging` | `logging` |
| `pathlib` | `Path` |
| `sqlalchemy` | `delete`, `select` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `types` | `SimpleNamespace` |
| `typing` | `Any`, `Literal`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/system_settings_service.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/system_settings_service.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (8) |
| Outbound | `backend` (5) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 0 |

> All 13 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [RuntimeSettingSource](../entities/system_settings_service_RuntimeSettingSource.md) | Type alias | 33 | `Literal['runtime', 'environment', 'default']` | — |
| [RuntimeSettingsError](../entities/RuntimeSettingsError.md) | Class | 38 | `ValueError` | Raised when a runtime settings update is invalid. |
| [RuntimeSettingsEncryptionError](../entities/RuntimeSettingsEncryptionError.md) | Class | 42 | `RuntimeSettingsError` | Raised when a secret cannot be encrypted or decrypted. |
| [SettingDefinition](../entities/SettingDefinition.md) | Class | 47 | — | Catalog definition for one writable runtime setting. |
| [RuntimeSettingsService](../entities/RuntimeSettingsService.md) | Class | 116 | — | Read, update, and resolve catalogued runtime system settings. |
