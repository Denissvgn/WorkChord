# UserSession

**Location:** `backend/app/models/user_session.py:15`
**Kind:** Class
**Bases:** `Base`
**Module:** [user_session](../modules/user_session.md)

## Description

Opaque browser identity with non-authoritative request audit metadata.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(primary_key=True)` | — |
| `public_id` | `Mapped[str]` | `mapped_column(String(24), unique=True, index=True, default=lambda: secrets.token_hex(6))` | — |
| `session_token_hash` | `Mapped[str \| None]` | `mapped_column(String(64), unique=True, index=True, nullable=True)` | — |
| `ip_address` | `Mapped[str]` | `mapped_column(String, index=True)` | — |
| `user_agent` | `Mapped[str \| None]` | `mapped_column(String, nullable=True)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now)` | — |
| `last_seen_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, onupdate=utc_now)` | — |
| `expires_at` | `Mapped[datetime \| None]` | `mapped_column(UTCDateTime(), nullable=True)` | — |
| `revoked_at` | `Mapped[datetime \| None]` | `mapped_column(UTCDateTime(), nullable=True)` | — |
| `saved_views` | `Mapped[list['SavedView']]` | `relationship('SavedView', back_populates='created_by_session')` | — |
| `project_updates` | `Mapped[list['ProjectUpdateEntry']]` | `relationship('ProjectUpdateEntry', back_populates='created_by_session')` | — |
| `plan_shares` | `Mapped[list['PlanShare']]` | `relationship('PlanShare', back_populates='created_by_session')` | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__repr__` | `() -> str` | — | — |
| `display_name` | `() -> str` | `@property` | Return a privacy-safe stable label without exposing IP or token data. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["UserSession (backend/app/models/user_session.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["backend/app/models/plan_share.py"]
    n4["backend/app/models/project.py"]
    n5["backend/app/models/saved_view.py"]
    n6["create_plan_share (backend/app/routers/plan_shares.py)"]
    n7["get_current_plan_share (backend/app/routers/plan_shares.py)"]
    n8["get_plan_share (backend/app/routers/plan_shares.py)"]
    n9["revoke_plan_share (backend/app/routers/plan_shares.py)"]
    n10["create_project_update (backend/app/routers/projects.py)"]
    n11["create_saved_view (backend/app/routers/saved_views.py)"]
    n12["delete_saved_view (backend/app/routers/saved_views.py)"]
    n13["duplicate_saved_view (backend/app/routers/saved_views.py)"]
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
    n13 --> n0
    click n0 "../modules/user_session.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/models_plan_share.md"
    click n4 "../modules/models_project.md"
    click n5 "../modules/models_saved_view.md"
    click n6 "../modules/plan_shares.md"
    click n7 "../modules/plan_shares.md"
    click n8 "../modules/plan_shares.md"
    click n9 "../modules/plan_shares.md"
    click n10 "../modules/projects.md"
    click n11 "../modules/saved_views.md"
    click n12 "../modules/saved_views.md"
    click n13 "../modules/saved_views.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [user_session](../modules/user_session.md) | 2 | `created_at`, `expires_at`, `id`, `ip_address`, `last_seen_at`, `plan_shares`, `project_updates`, `public_id`, `revoked_at`, `saved_views`, `session_token_hash`, `user_agent` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `plan_share` | import | [models_plan_share](../modules/models_plan_share.md) | — |
| `project` | import | [models_project](../modules/models_project.md) | — |
| `saved_view` | import | [models_saved_view](../modules/models_saved_view.md) | — |
| `create_plan_share` | type_reference | [plan_shares](../modules/plan_shares.md) | — |
| `get_current_plan_share` | type_reference | [plan_shares](../modules/plan_shares.md) | — |
| `get_plan_share` | type_reference | [plan_shares](../modules/plan_shares.md) | — |
| `revoke_plan_share` | type_reference | [plan_shares](../modules/plan_shares.md) | — |
| `create_project_update` | type_reference | [projects](../modules/projects.md) | — |
| `create_saved_view` | type_reference | [saved_views](../modules/saved_views.md) | — |
| `delete_saved_view` | type_reference | [saved_views](../modules/saved_views.md) | — |
| `duplicate_saved_view` | type_reference | [saved_views](../modules/saved_views.md) | — |

> References: showing 12 of 37 logical references; 25 omitted by the 12-row generated summary limit.
