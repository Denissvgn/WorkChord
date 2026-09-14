# SystemSettingsResponse

**Location:** `backend/app/schemas/system_settings.py:114`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_system_settings](../modules/schemas_system_settings.md)

## Description

Runtime configuration summary.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `app` | `AppRuntimeSettingsResponse` | `app` | Yes | No | — | — | — | — |
| `llm` | `LLMRuntimeSettingsResponse` | `llm` | Yes | No | — | — | — | — |
| `github` | `GitHubRuntimeSettingsResponse` | `github` | Yes | No | — | — | — | — |
| `web_intake` | `WebIntakeRuntimeSettingsResponse` | `web_intake` | Yes | No | — | — | — | — |
| `restart_required` | `list[RestartRequiredSetting]` | `restart_required` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SystemSettingsResponse (backend/app/schemas/system_settings.py)"]
    n1["BaseModel"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["get_system_settings (backend/app/routers/system_settings.py)"]
    n4["backend/app/schemas/__init__.py"]
    n5["RuntimeSettingsService.system_response (backend/app/services/system_settings_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/schemas_system_settings.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_system_settings.md"
    click n4 "../modules/schemas___init__.md"
    click n5 "../modules/system_settings_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_system_settings](../modules/schemas_system_settings.md) | 0 | `app`, `github`, `llm`, `restart_required`, `web_intake` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `get_system_settings` | type_reference | [routers_system_settings](../modules/routers_system_settings.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `RuntimeSettingsService.system_response` | call | [system_settings_service](../modules/system_settings_service.md) | 1 |
| `RuntimeSettingsService.system_response` | type_reference | [system_settings_service](../modules/system_settings_service.md) | — |
