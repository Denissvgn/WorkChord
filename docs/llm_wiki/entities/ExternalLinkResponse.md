# ExternalLinkResponse

**Location:** `backend/app/schemas/external_link.py:116`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_external_link](../modules/schemas_external_link.md)

## Description

Schema for external link responses, including synthetic legacy links.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `from_attributes` | `True` | model_config |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `id` | `Optional[int]` | `id` | No | Yes | `None` | — | — | — |
| `entity_type` | `str` | `entity_type` | Yes | No | — | — | — | — |
| `entity_id` | `int` | `entity_id` | Yes | No | — | — | — | — |
| `provider` | `str` | `provider` | Yes | No | — | — | — | — |
| `external_key` | `Optional[str]` | `external_key` | No | Yes | `None` | — | — | — |
| `url` | `Optional[str]` | `url` | No | Yes | `None` | — | — | — |
| `title` | `Optional[str]` | `title` | No | Yes | `None` | — | — | — |
| `status` | `Optional[str]` | `status` | No | Yes | `None` | — | — | — |
| `metadata_json` | `dict[str, Any]` | `metadata_json` | No | No | factory: `dict` | — | — | — |
| `is_legacy` | `bool` | `is_legacy` | No | No | `False` | — | — | — |
| `created_at` | `Optional[datetime]` | `created_at` | No | Yes | `None` | — | — | — |
| `updated_at` | `Optional[datetime]` | `updated_at` | No | Yes | `None` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ExternalLinkResponse (backend/app/schemas/external_link.py)"]
    n1["BaseModel"]
    n2["create_task_external_link (backend/app/routers/tasks.py)"]
    n3["create_task_github_external_link (backend/app/routers/tasks.py)"]
    n4["list_task_external_links (backend/app/routers/tasks.py)"]
    n5["refresh_github_external_link (backend/app/routers/tasks.py)"]
    n6["update_external_link (backend/app/routers/tasks.py)"]
    n7["backend/app/schemas/__init__.py"]
    n8["backend/app/schemas/task.py"]
    n9["ExternalLinkService.legacy_task_link_response (backend/app/services/external_link_service.py)"]
    n10["ExternalLinkService.link_to_response (backend/app/services/external_link_service.py)"]
    n11["ExternalLinkService.task_links_to_response (backend/app/services/external_link_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    click n0 "../modules/schemas_external_link.md"
    click n2 "../modules/tasks.md"
    click n3 "../modules/tasks.md"
    click n4 "../modules/tasks.md"
    click n5 "../modules/tasks.md"
    click n6 "../modules/tasks.md"
    click n7 "../modules/schemas___init__.md"
    click n8 "../modules/schemas_task.md"
    click n9 "../modules/external_link_service.md"
    click n10 "../modules/external_link_service.md"
    click n11 "../modules/external_link_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_external_link](../modules/schemas_external_link.md) | 0 | `created_at`, `entity_id`, `entity_type`, `external_key`, `id`, `is_legacy`, `metadata_json`, `provider`, `status`, `title`, `updated_at`, `url` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_task_external_link` | type_reference | [tasks](../modules/tasks.md) | — |
| `create_task_github_external_link` | type_reference | [tasks](../modules/tasks.md) | — |
| `list_task_external_links` | type_reference | [tasks](../modules/tasks.md) | — |
| `refresh_github_external_link` | type_reference | [tasks](../modules/tasks.md) | — |
| `update_external_link` | type_reference | [tasks](../modules/tasks.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `task` | import | [schemas_task](../modules/schemas_task.md) | — |
| `ExternalLinkService.legacy_task_link_response` | call | [external_link_service](../modules/external_link_service.md) | 1 |
| `ExternalLinkService.legacy_task_link_response` | type_reference | [external_link_service](../modules/external_link_service.md) | — |
| `ExternalLinkService.link_to_response` | call | [external_link_service](../modules/external_link_service.md) | 1 |
| `ExternalLinkService.link_to_response` | type_reference | [external_link_service](../modules/external_link_service.md) | — |
| `ExternalLinkService.task_links_to_response` | type_reference | [external_link_service](../modules/external_link_service.md) | — |
