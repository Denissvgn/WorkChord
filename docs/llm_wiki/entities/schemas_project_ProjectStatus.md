# ProjectStatus

**Location:** `backend/app/schemas/project.py:11`
**Kind:** Enum
**Bases:** `str`, `Enum`
**Module:** [schemas_project](../modules/schemas_project.md)

## Description

Project lifecycle status.

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `PROPOSED` | `'proposed'` | — |
| `PLANNED` | `'planned'` | — |
| `ACTIVE` | `'active'` | — |
| `PAUSED` | `'paused'` | — |
| `COMPLETED` | `'completed'` | — |
| `CANCELED` | `'canceled'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProjectStatus (backend/app/schemas/project.py)"]
    n1["Enum"]
    n2["str"]
    n3["backend/app/schemas/__init__.py"]
    n0 --> n1
    n0 --> n2
    n3 --> n0
    click n0 "../modules/schemas_project.md"
    click n3 "../modules/schemas___init__.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_project](../modules/schemas_project.md) | 0 | `ACTIVE`, `CANCELED`, `COMPLETED`, `PAUSED`, `PLANNED`, `PROPOSED` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Enum` | — |
| Base | `str` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
