# ReleaseUpdateRequest

**Location:** `backend/app/schemas/release.py:77`
**Kind:** Pydantic model
**Bases:** `ReleaseUpdate`
**Module:** [schemas_release](../modules/schemas_release.md)

## Description

API request for partially updating a release.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ReleaseUpdateRequest (backend/app/schemas/release.py)"]
    n1["ReleaseUpdate (backend/app/schemas/release.py)"]
    n2["update_release (backend/app/routers/projects.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["ReleaseService.update (backend/app/services/release_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_release.md"
    click n1 "../modules/schemas_release.md"
    click n2 "../modules/projects.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/release_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_release](../modules/schemas_release.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ReleaseUpdate` | [schemas_release](../modules/schemas_release.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `update_release` | type_reference | [projects](../modules/projects.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `ReleaseService.update` | type_reference | [release_service](../modules/release_service.md) | — |
