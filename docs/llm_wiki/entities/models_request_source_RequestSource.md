# RequestSource

**Location:** `backend/app/models/request_source.py:37`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_request_source](../modules/models_request_source.md)

## Description

Free-text source record that can be linked to work entities.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=True)` | — |
| `title` | `Mapped[str]` | `mapped_column(String(500), nullable=False)` | — |
| `description` | `Mapped[Optional[str]]` | `mapped_column(Text, nullable=True)` | — |
| `source_type` | `Mapped[str]` | `mapped_column(String(50), nullable=False, index=True)` | — |
| `source_name` | `Mapped[Optional[str]]` | `mapped_column(String(255), nullable=True)` | — |
| `source_url` | `Mapped[Optional[str]]` | `mapped_column(String(1000), nullable=True, index=True)` | — |
| `external_key` | `Mapped[Optional[str]]` | `mapped_column(String(255), nullable=True, index=True)` | — |
| `priority_hint` | `Mapped[Optional[int]]` | `mapped_column(Integer, nullable=True)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, nullable=False, index=True)` | — |
| `links` | `Mapped[list['RequestSourceLink']]` | `relationship('RequestSourceLink', back_populates='request_source', cascade='all, delete-orphan', passive_deletes=True, order_by='RequestSourceLink.created_at, RequestSourceLink.id')` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RequestSource (backend/app/models/request_source.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["RequestSourceService._get_source_or_raise (backend/app/services/request_source_service.py)"]
    n4["RequestSourceService._normalize_target_type (backend/app/services/request_source_service.py)"]
    n5["RequestSourceService._require_target_exists (backend/app/services/request_source_service.py)"]
    n6["RequestSourceService._source_from_payload (backend/app/services/request_source_service.py)"]
    n7["RequestSourceService._source_from_triage_item (backend/app/services/request_source_service.py)"]
    n8["RequestSourceService._target_model_and_field (backend/app/services/request_source_service.py)"]
    n9["RequestSourceService.create_link (backend/app/services/request_source_service.py)"]
    n10["RequestSourceService.get_link (backend/app/services/request_source_service.py)"]
    n11["RequestSourceService.link_triage_item_as_task_request (backend/app/services/request_source_service.py)"]
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
    click n0 "../modules/models_request_source.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/request_source_service.md"
    click n4 "../modules/request_source_service.md"
    click n5 "../modules/request_source_service.md"
    click n6 "../modules/request_source_service.md"
    click n7 "../modules/request_source_service.md"
    click n8 "../modules/request_source_service.md"
    click n9 "../modules/request_source_service.md"
    click n10 "../modules/request_source_service.md"
    click n11 "../modules/request_source_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_request_source](../modules/models_request_source.md) | 0 | `created_at`, `description`, `external_key`, `id`, `links`, `priority_hint`, `source_name`, `source_type`, `source_url`, `title` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `RequestSourceService._get_source_or_raise` | type_reference | [request_source_service](../modules/request_source_service.md) | — |
| `RequestSourceService._normalize_target_type` | type_reference | [request_source_service](../modules/request_source_service.md) | — |
| `RequestSourceService._require_target_exists` | type_reference | [request_source_service](../modules/request_source_service.md) | — |
| `RequestSourceService._source_from_payload` | call | [request_source_service](../modules/request_source_service.md) | 1 |
| `RequestSourceService._source_from_payload` | type_reference | [request_source_service](../modules/request_source_service.md) | — |
| `RequestSourceService._source_from_triage_item` | call | [request_source_service](../modules/request_source_service.md) | 1 |
| `RequestSourceService._source_from_triage_item` | type_reference | [request_source_service](../modules/request_source_service.md) | — |
| `RequestSourceService._target_model_and_field` | type_reference | [request_source_service](../modules/request_source_service.md) | — |
| `RequestSourceService.create_link` | type_reference | [request_source_service](../modules/request_source_service.md) | — |
| `RequestSourceService.get_link` | type_reference | [request_source_service](../modules/request_source_service.md) | — |
| `RequestSourceService.link_triage_item_as_task_request` | type_reference | [request_source_service](../modules/request_source_service.md) | — |

> References: showing 12 of 14 logical references; 2 omitted by the 12-row generated summary limit.
