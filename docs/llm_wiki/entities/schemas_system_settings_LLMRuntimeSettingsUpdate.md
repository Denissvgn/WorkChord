# LLMRuntimeSettingsUpdate

**Location:** `backend/app/schemas/system_settings.py:37`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_system_settings](../modules/schemas_system_settings.md)

## Description

Update request for LLM runtime settings.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `provider` | `LLMProvider \| None` | `provider` | No | Yes | `None` | — | — | — |
| `api_url` | `str \| None` | `api_url` | No | Yes | `None` | — | — | — |
| `model` | `str \| None` | `model` | No | Yes | `None` | — | — | — |
| `temperature` | `float \| None` | `temperature` | No | Yes | `None` | ge=0; le=2 | — | — |
| `max_output_tokens` | `int \| None` | `max_output_tokens` | No | Yes | `None` | ge=256; le=12000 | — | — |
| `api_key` | `str \| None` | `api_key` | No | Yes | `None` | — | — | — |
| `clear_api_key` | `bool` | `clear_api_key` | No | No | `False` | — | — | — |
| `reset_fields` | `list[str]` | `reset_fields` | No | No | factory: `list` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["LLMRuntimeSettingsUpdate (backend/app/schemas/system_settings.py)"]
    n1["BaseModel"]
    n2["update_llm_settings (backend/app/routers/system_settings.py)"]
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
| [schemas_system_settings](../modules/schemas_system_settings.md) | 0 | `api_key`, `api_url`, `clear_api_key`, `max_output_tokens`, `model`, `provider`, `reset_fields`, `temperature` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `update_llm_settings` | type_reference | [routers_system_settings](../modules/routers_system_settings.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
