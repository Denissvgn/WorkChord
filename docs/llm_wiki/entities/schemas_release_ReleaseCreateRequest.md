# ReleaseCreateRequest

**Location:** `backend/app/schemas/release.py:47`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_release](../modules/schemas_release.md)

## Description

API request for creating a project-scoped release.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `name` | `str` | `name` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `description` | `Optional[str]` | `description` | No | Yes | `None` | — | — | — |
| `status` | `ReleaseStatus` | `status` | No | No | `ReleaseStatus.PLANNED` | — | — | — |
| `target_date` | `Optional[date]` | `target_date` | No | Yes | `None` | — | — | — |
| `shipped_at` | `Optional[datetime]` | `shipped_at` | No | Yes | `None` | — | — | — |
| `version` | `Optional[str]` | `version` | No | Yes | `None` | max_length=100 | — | — |
| `environment` | `Optional[str]` | `environment` | No | Yes | `None` | max_length=100 | — | — |
| `task_ids` | `list[int]` | `task_ids` | No | No | factory: `list` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ReleaseCreateRequest (backend/app/schemas/release.py)"]
    n1["BaseModel"]
    n2["create_project_release (backend/app/routers/projects.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["ReleaseService.create_for_project (backend/app/services/release_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_release.md"
    click n2 "../modules/projects.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/release_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_release](../modules/schemas_release.md) | 0 | `description`, `environment`, `name`, `shipped_at`, `status`, `target_date`, `task_ids`, `version` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_project_release` | type_reference | [projects](../modules/projects.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `ReleaseService.create_for_project` | type_reference | [release_service](../modules/release_service.md) | — |
