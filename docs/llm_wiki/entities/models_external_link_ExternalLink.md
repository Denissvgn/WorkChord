# ExternalLink

**Location:** `backend/app/models/external_link.py:29`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_external_link](../modules/models_external_link.md)

## Description

Generic link from an internal entity to an external delivery artifact.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=True)` | — |
| `entity_type` | `Mapped[str]` | `mapped_column(String(50), nullable=False)` | — |
| `entity_id` | `Mapped[int]` | `mapped_column(Integer, nullable=False)` | — |
| `provider` | `Mapped[str]` | `mapped_column(String(50), nullable=False)` | — |
| `external_key` | `Mapped[Optional[str]]` | `mapped_column(String(255), nullable=True)` | — |
| `url` | `Mapped[Optional[str]]` | `mapped_column(String(1000), nullable=True, index=True)` | — |
| `title` | `Mapped[Optional[str]]` | `mapped_column(String(500), nullable=True)` | — |
| `status` | `Mapped[Optional[str]]` | `mapped_column(String(100), nullable=True)` | — |
| `metadata_json` | `Mapped[dict[str, Any]]` | `mapped_column(JSON, default=dict, nullable=False)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, nullable=False)` | — |
| `updated_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False, index=True)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ExternalLink (backend/app/models/external_link.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["backend/app/models/release.py"]
    n4["backend/app/models/task.py"]
    n5["ExternalLinkService.create (backend/app/services/external_link_service.py)"]
    n6["ExternalLinkService.create_task_github_link (backend/app/services/external_link_service.py)"]
    n7["ExternalLinkService.create_task_link (backend/app/services/external_link_service.py)"]
    n8["ExternalLinkService.get_by_id (backend/app/services/external_link_service.py)"]
    n9["ExternalLinkService.legacy_task_link_response (backend/app/services/external_link_service.py)"]
    n10["ExternalLinkService.link_to_response (backend/app/services/external_link_service.py)"]
    n11["ExternalLinkService.list_for_entity (backend/app/services/external_link_service.py)"]
    n12["ExternalLinkService.list_task_links (backend/app/services/external_link_service.py)"]
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
    n12 --> n0
    click n0 "../modules/models_external_link.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/models_release.md"
    click n4 "../modules/models_task.md"
    click n5 "../modules/external_link_service.md"
    click n6 "../modules/external_link_service.md"
    click n7 "../modules/external_link_service.md"
    click n8 "../modules/external_link_service.md"
    click n9 "../modules/external_link_service.md"
    click n10 "../modules/external_link_service.md"
    click n11 "../modules/external_link_service.md"
    click n12 "../modules/external_link_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_external_link](../modules/models_external_link.md) | 0 | `created_at`, `entity_id`, `entity_type`, `external_key`, `id`, `metadata_json`, `provider`, `status`, `title`, `updated_at`, `url` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `release` | import | [models_release](../modules/models_release.md) | — |
| `task` | import | [models_task](../modules/models_task.md) | — |
| `ExternalLinkService.create` | call | [external_link_service](../modules/external_link_service.md) | 1 |
| `ExternalLinkService.create` | type_reference | [external_link_service](../modules/external_link_service.md) | — |
| `ExternalLinkService.create_task_github_link` | type_reference | [external_link_service](../modules/external_link_service.md) | — |
| `ExternalLinkService.create_task_link` | type_reference | [external_link_service](../modules/external_link_service.md) | — |
| `ExternalLinkService.get_by_id` | type_reference | [external_link_service](../modules/external_link_service.md) | — |
| `ExternalLinkService.legacy_task_link_response` | type_reference | [external_link_service](../modules/external_link_service.md) | — |
| `ExternalLinkService.link_to_response` | type_reference | [external_link_service](../modules/external_link_service.md) | — |
| `ExternalLinkService.list_for_entity` | type_reference | [external_link_service](../modules/external_link_service.md) | — |
| `ExternalLinkService.list_task_links` | type_reference | [external_link_service](../modules/external_link_service.md) | — |

> References: showing 12 of 20 logical references; 8 omitted by the 12-row generated summary limit.
