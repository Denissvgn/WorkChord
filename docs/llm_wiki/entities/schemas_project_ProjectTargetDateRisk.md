# ProjectTargetDateRisk

**Location:** `backend/app/schemas/project.py:33`
**Kind:** Enum
**Bases:** `str`, `Enum`
**Module:** [schemas_project](../modules/schemas_project.md)

## Description

Target-date risk for project delivery.

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
    n0["ProjectTargetDateRisk (backend/app/schemas/project.py)"]
    n1["Enum"]
    n2["str"]
    n3["backend/app/schemas/__init__.py"]
    n4["ProjectService._calculate_target_date_risk (backend/app/services/project_service.py)"]
    n0 --> n1
    n0 --> n2
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_project.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/project_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_project](../modules/schemas_project.md) | 0 | `AT_RISK`, `OFF_TRACK`, `ON_TRACK`, `UNKNOWN` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Enum` | — |
| Base | `str` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `ProjectService._calculate_target_date_risk` | type_reference | [project_service](../modules/project_service.md) | — |
