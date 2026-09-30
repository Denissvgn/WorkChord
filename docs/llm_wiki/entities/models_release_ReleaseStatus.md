# ReleaseStatus

**Location:** `backend/app/models/release.py:29`
**Kind:** Enum
**Bases:** `str`, `Enum`
**Module:** [models_release](../modules/models_release.md)

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
    n0["ReleaseStatus (backend/app/models/release.py)"]
    n1["Enum"]
    n2["str"]
    n3["backend/app/models/__init__.py"]
    n4["backend/app/services/release_service.py"]
    n0 --> n1
    n0 --> n2
    n3 --> n0
    n4 --> n0
    click n0 "../modules/models_release.md"
    click n3 "../modules/models___init__.md"
    click n4 "../modules/release_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_release](../modules/models_release.md) | 0 | `BUILDING`, `CANCELED`, `PLANNED`, `SHIPPED` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Enum` | — |
| Base | `str` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `release_service` | import | [release_service](../modules/release_service.md) | — |
