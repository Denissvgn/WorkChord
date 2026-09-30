# ReleaseStatus

**Location:** `backend/app/schemas/release.py:11`
**Kind:** Enum
**Bases:** `str`, `Enum`
**Module:** [schemas_release](../modules/schemas_release.md)

## Description

Release lifecycle independent of task status.

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `PLANNED` | `'planned'` | — |
| `BUILDING` | `'building'` | — |
| `SHIPPED` | `'shipped'` | — |
| `CANCELED` | `'canceled'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ReleaseStatus (backend/app/schemas/release.py)"]
    n1["Enum"]
    n2["str"]
    n3["backend/app/schemas/__init__.py"]
    n0 --> n1
    n0 --> n2
    n3 --> n0
    click n0 "../modules/schemas_release.md"
    click n3 "../modules/schemas___init__.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_release](../modules/schemas_release.md) | 0 | `BUILDING`, `CANCELED`, `PLANNED`, `SHIPPED` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Enum` | — |
| Base | `str` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
