# ExternalLinkProvider

**Location:** `backend/app/schemas/external_link.py:27`
**Kind:** Enum
**Bases:** `str`, `Enum`
**Module:** [schemas_external_link](../modules/schemas_external_link.md)

## Description

Supported external link providers.

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `GITHUB` | `'github'` | — |
| `GITLAB` | `'gitlab'` | — |
| `FIGMA` | `'figma'` | — |
| `SENTRY` | `'sentry'` | — |
| `CUSTOM` | `'custom'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ExternalLinkProvider (backend/app/schemas/external_link.py)"]
    n1["Enum"]
    n2["str"]
    n3["backend/app/schemas/__init__.py"]
    n4["backend/app/services/external_link_service.py"]
    n0 --> n1
    n0 --> n2
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_external_link.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/external_link_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_external_link](../modules/schemas_external_link.md) | 0 | `CUSTOM`, `FIGMA`, `GITHUB`, `GITLAB`, `SENTRY` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Enum` | — |
| Base | `str` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `external_link_service` | import | [external_link_service](../modules/external_link_service.md) | — |
