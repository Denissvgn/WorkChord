# Release

**Location:** `backend/app/models/release.py:60`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_release](../modules/models_release.md)

## Description

Lightweight shipping record scoped to one project.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=True)` | — |
| `name` | `Mapped[str]` | `mapped_column(String(255), nullable=False)` | — |
| `description` | `Mapped[Optional[str]]` | `mapped_column(Text, nullable=True)` | — |
| `project_id` | `Mapped[int]` | `mapped_column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, index=True)` | — |
| `status` | `Mapped[str]` | `mapped_column(String(50), default=ReleaseStatus.PLANNED.value, nullable=False, index=True)` | — |
| `target_date` | `Mapped[Optional[date]]` | `mapped_column(Date, nullable=True, index=True)` | — |
| `shipped_at` | `Mapped[Optional[datetime]]` | `mapped_column(UTCDateTime(), nullable=True)` | — |
| `version` | `Mapped[Optional[str]]` | `mapped_column(String(100), nullable=True)` | — |
| `environment` | `Mapped[Optional[str]]` | `mapped_column(String(100), nullable=True)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, nullable=False)` | — |
| `updated_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False)` | — |
| `project` | `Mapped['Project']` | `relationship('Project', back_populates='releases')` | — |
| `tasks` | `Mapped[list['Task']]` | `relationship('Task', secondary=release_tasks, order_by='Task.sort_order, Task.id')` | — |
| `external_links` | `Mapped[list['ExternalLink']]` | `relationship('ExternalLink', primaryjoin=lambda: and_(Release.id == foreign(ExternalLink.entity_id), ExternalLink.entity_type == 'release'), order_by='ExternalLink.created_at, ExternalLink.id', viewonly=True)` | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `task_ids` | `() -> list[int]` | `@property` | Return linked task IDs for response schemas and future service code. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Release (backend/app/models/release.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["backend/app/models/project.py"]
    n4["ReleaseService._emit_release_shipped_events (backend/app/services/release_service.py)"]
    n5["ReleaseService._is_shipped (backend/app/services/release_service.py)"]
    n6["ReleaseService._release_shipped_payload (backend/app/services/release_service.py)"]
    n7["ReleaseService.create_for_project (backend/app/services/release_service.py)"]
    n8["ReleaseService.get_by_id (backend/app/services/release_service.py)"]
    n9["ReleaseService.list_for_project (backend/app/services/release_service.py)"]
    n10["ReleaseService.update (backend/app/services/release_service.py)"]
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
    click n0 "../modules/models_release.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/models_project.md"
    click n4 "../modules/release_service.md"
    click n5 "../modules/release_service.md"
    click n6 "../modules/release_service.md"
    click n7 "../modules/release_service.md"
    click n8 "../modules/release_service.md"
    click n9 "../modules/release_service.md"
    click n10 "../modules/release_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_release](../modules/models_release.md) | 1 | `created_at`, `description`, `environment`, `external_links`, `id`, `name`, `project`, `project_id`, `shipped_at`, `status`, `target_date`, `tasks` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `project` | import | [models_project](../modules/models_project.md) | — |
| `ReleaseService._emit_release_shipped_events` | type_reference | [release_service](../modules/release_service.md) | — |
| `ReleaseService._is_shipped` | type_reference | [release_service](../modules/release_service.md) | — |
| `ReleaseService._release_shipped_payload` | type_reference | [release_service](../modules/release_service.md) | — |
| `ReleaseService.create_for_project` | call | [release_service](../modules/release_service.md) | 1 |
| `ReleaseService.create_for_project` | type_reference | [release_service](../modules/release_service.md) | — |
| `ReleaseService.get_by_id` | type_reference | [release_service](../modules/release_service.md) | — |
| `ReleaseService.list_for_project` | type_reference | [release_service](../modules/release_service.md) | — |
| `ReleaseService.update` | type_reference | [release_service](../modules/release_service.md) | — |
