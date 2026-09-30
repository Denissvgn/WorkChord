# ExternalLinkProvider

**Location:** `backend/app/models/external_link.py:20`
**Kind:** Enum
**Bases:** `str`, `Enum`
**Module:** [models_external_link](../modules/models_external_link.md)

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
    n0["ExternalLinkProvider (backend/app/models/external_link.py)"]
    n1["Enum"]
    n2["str"]
    n3["backend/app/models/__init__.py"]
    n0 --> n1
    n0 --> n2
    n3 --> n0
    click n0 "../modules/models_external_link.md"
    click n3 "../modules/models___init__.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_external_link](../modules/models_external_link.md) | 0 | `CUSTOM`, `FIGMA`, `GITHUB`, `GITLAB`, `SENTRY` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Enum` | — |
| Base | `str` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
