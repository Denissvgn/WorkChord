# ProjectHealth

**Location:** `backend/app/models/project.py:32`
**Kind:** Enum
**Bases:** `str`, `Enum`
**Module:** [models_project](../modules/models_project.md)

## Description

Project delivery health.

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `UNKNOWN` | `'unknown'` | — |
| `ON_TRACK` | `'on_track'` | — |
| `AT_RISK` | `'at_risk'` | — |
| `OFF_TRACK` | `'off_track'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProjectHealth (backend/app/models/project.py)"]
    n1["Enum"]
    n2["str"]
    n3["backend/app/models/__init__.py"]
    n0 --> n1
    n0 --> n2
    n3 --> n0
    click n0 "../modules/models_project.md"
    click n3 "../modules/models___init__.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_project](../modules/models_project.md) | 0 | `AT_RISK`, `OFF_TRACK`, `ON_TRACK`, `UNKNOWN` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Enum` | — |
| Base | `str` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
