# GitHubRuntimeSettingsUpdate

**Location:** `backend/app/schemas/system_settings.py:61`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_system_settings](../modules/schemas_system_settings.md)

## Description

Update request for GitHub runtime settings.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `api_url` | `str \| None` | `api_url` | No | Yes | `None` | — | — | — |
| `token` | `str \| None` | `token` | No | Yes | `None` | — | — | — |
| `clear_token` | `bool` | `clear_token` | No | No | `False` | — | — | — |
| `request_timeout_seconds` | `float \| None` | `request_timeout_seconds` | No | Yes | `None` | gt=0; le=120 | — | — |
| `webhook_secret` | `str \| None` | `webhook_secret` | No | Yes | `None` | — | — | — |
| `clear_webhook_secret` | `bool` | `clear_webhook_secret` | No | No | `False` | — | — | — |
| `webhook_create_triage_for_unmatched` | `bool \| None` | `webhook_create_triage_for_unmatched` | No | Yes | `None` | — | — | — |
| `reset_fields` | `list[str]` | `reset_fields` | No | No | factory: `list` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GitHubRuntimeSettingsUpdate (backend/app/schemas/system_settings.py)"]
    n1["BaseModel"]
    n2["update_github_settings (backend/app/routers/system_settings.py)"]
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
| [schemas_system_settings](../modules/schemas_system_settings.md) | 0 | `api_url`, `clear_token`, `clear_webhook_secret`, `request_timeout_seconds`, `reset_fields`, `token`, `webhook_create_triage_for_unmatched`, `webhook_secret` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `update_github_settings` | type_reference | [routers_system_settings](../modules/routers_system_settings.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
