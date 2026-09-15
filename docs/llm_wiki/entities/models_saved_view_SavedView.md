# SavedView

**Location:** `backend/app/models/saved_view.py:30`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_saved_view](../modules/models_saved_view.md)

## Description

Persisted filter, sort, and column configuration for reusable views.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=True)` | — |
| `name` | `Mapped[str]` | `mapped_column(String(255), nullable=False)` | — |
| `description` | `Mapped[Optional[str]]` | `mapped_column(Text, nullable=True)` | — |
| `seed_key` | `Mapped[Optional[str]]` | `mapped_column(String(100), nullable=True, unique=True, index=True)` | — |
| `view_type` | `Mapped[str]` | `mapped_column(String(50), nullable=False, index=True)` | — |
| `scope` | `Mapped[str]` | `mapped_column(String(50), nullable=False, index=True)` | — |
| `filters_json` | `Mapped[dict[str, Any]]` | `mapped_column(JSON, default=dict, nullable=False)` | — |
| `sort_json` | `Mapped[dict[str, Any]]` | `mapped_column(JSON, default=dict, nullable=False)` | — |
| `columns_json` | `Mapped[dict[str, Any]]` | `mapped_column(JSON, default=dict, nullable=False)` | — |
| `created_by_session_id` | `Mapped[Optional[int]]` | `mapped_column(Integer, ForeignKey('user_sessions.id', ondelete='SET NULL'), nullable=True, index=True)` | — |
| `schema_version` | `Mapped[int]` | `mapped_column(Integer, default=1, nullable=False)` | — |
| `metric_migration_note` | `Mapped[str \| None]` | `mapped_column(String(64))` | — |
| `owner_principal_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('principals.id', ondelete='RESTRICT'), index=True)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, nullable=False, index=True)` | — |
| `updated_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False, index=True)` | — |
| `created_by_session` | `Mapped[Optional['UserSession']]` | `relationship('UserSession', back_populates='saved_views')` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SavedView (backend/app/models/saved_view.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["backend/app/models/user_session.py"]
    n4["SavedViewService._can_write (backend/app/services/saved_view_service.py)"]
    n5["SavedViewService._dashboard_count (backend/app/services/saved_view_service.py)"]
    n6["SavedViewService._is_visible_to_session (backend/app/services/saved_view_service.py)"]
    n7["SavedViewService._reject_system_scope (backend/app/services/saved_view_service.py)"]
    n8["SavedViewService._require_personal_creator (backend/app/services/saved_view_service.py)"]
    n9["SavedViewService._response_for_view (backend/app/services/saved_view_service.py)"]
    n10["SavedViewService._target_path_for_view (backend/app/services/saved_view_service.py)"]
    n11["SavedViewService.create (backend/app/services/saved_view_service.py)"]
    n12["SavedViewService.create_for_session (backend/app/services/saved_view_service.py)"]
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
    click n0 "../modules/models_saved_view.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/user_session.md"
    click n4 "../modules/saved_view_service.md"
    click n5 "../modules/saved_view_service.md"
    click n6 "../modules/saved_view_service.md"
    click n7 "../modules/saved_view_service.md"
    click n8 "../modules/saved_view_service.md"
    click n9 "../modules/saved_view_service.md"
    click n10 "../modules/saved_view_service.md"
    click n11 "../modules/saved_view_service.md"
    click n12 "../modules/saved_view_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_saved_view](../modules/models_saved_view.md) | 0 | `columns_json`, `created_at`, `created_by_session`, `created_by_session_id`, `description`, `filters_json`, `id`, `metric_migration_note`, `name`, `owner_principal_id`, `schema_version`, `scope` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `user_session` | import | [user_session](../modules/user_session.md) | — |
| `SavedViewService._can_write` | type_reference | [saved_view_service](../modules/saved_view_service.md) | — |
| `SavedViewService._dashboard_count` | type_reference | [saved_view_service](../modules/saved_view_service.md) | — |
| `SavedViewService._is_visible_to_session` | type_reference | [saved_view_service](../modules/saved_view_service.md) | — |
| `SavedViewService._reject_system_scope` | type_reference | [saved_view_service](../modules/saved_view_service.md) | — |
| `SavedViewService._require_personal_creator` | type_reference | [saved_view_service](../modules/saved_view_service.md) | — |
| `SavedViewService._response_for_view` | type_reference | [saved_view_service](../modules/saved_view_service.md) | — |
| `SavedViewService._target_path_for_view` | type_reference | [saved_view_service](../modules/saved_view_service.md) | — |
| `SavedViewService.create` | call | [saved_view_service](../modules/saved_view_service.md) | 1 |
| `SavedViewService.create` | type_reference | [saved_view_service](../modules/saved_view_service.md) | — |
| `SavedViewService.create_for_session` | type_reference | [saved_view_service](../modules/saved_view_service.md) | — |

> References: showing 12 of 27 logical references; 15 omitted by the 12-row generated summary limit.
