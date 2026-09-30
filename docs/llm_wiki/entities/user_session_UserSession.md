# UserSession

**Location:** `backend/app/models/user_session.py:16`
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
| `principal_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('principals.id', ondelete='RESTRICT'), index=True)` | — |
| `csrf_token` | `Mapped[str \| None]` | `mapped_column(String(128))` | — |
| `authenticated_at` | `Mapped[datetime \| None]` | `mapped_column(UTCDateTime())` | — |
| `principal` | `Mapped['Principal \| None']` | `relationship('Principal', lazy='selectin')` | — |
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
| `authenticated` | `() -> bool` | `@property` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["UserSession (backend/app/models/user_session.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/http_authority.py"]
    n3["backend/app/models/__init__.py"]
    n4["backend/app/models/plan_share.py"]
    n5["backend/app/models/project.py"]
    n6["backend/app/models/saved_view.py"]
    n7["backend/app/routers/identity.py"]
    n8["create_plan_share (backend/app/routers/plan_shares.py)"]
    n9["get_current_plan_share (backend/app/routers/plan_shares.py)"]
    n10["revoke_plan_share (backend/app/routers/plan_shares.py)"]
    n11["create_project_update (backend/app/routers/projects.py)"]
    n12["create_saved_view (backend/app/routers/saved_views.py)"]
    n13["delete_saved_view (backend/app/routers/saved_views.py)"]
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
    click n2 "../modules/http_authority.md"
    click n3 "../modules/models___init__.md"
    click n4 "../modules/models_plan_share.md"
    click n5 "../modules/models_project.md"
    click n6 "../modules/models_saved_view.md"
    click n7 "../modules/routers_identity.md"
    click n8 "../modules/plan_shares.md"
    click n9 "../modules/plan_shares.md"
    click n10 "../modules/plan_shares.md"
    click n11 "../modules/projects.md"
    click n12 "../modules/saved_views.md"
    click n13 "../modules/saved_views.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [user_session](../modules/user_session.md) | 3 | `authenticated_at`, `created_at`, `csrf_token`, `expires_at`, `id`, `ip_address`, `last_seen_at`, `plan_shares`, `principal`, `principal_id`, `project_updates`, `public_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `http_authority` | import | [http_authority](../modules/http_authority.md) | — |
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `plan_share` | import | [models_plan_share](../modules/models_plan_share.md) | — |
| `project` | import | [models_project](../modules/models_project.md) | — |
| `saved_view` | import | [models_saved_view](../modules/models_saved_view.md) | — |
| `identity` | import | [routers_identity](../modules/routers_identity.md) | — |
| `create_plan_share` | type_reference | [plan_shares](../modules/plan_shares.md) | — |
| `get_current_plan_share` | type_reference | [plan_shares](../modules/plan_shares.md) | — |
| `revoke_plan_share` | type_reference | [plan_shares](../modules/plan_shares.md) | — |
| `create_project_update` | type_reference | [projects](../modules/projects.md) | — |
| `create_saved_view` | type_reference | [saved_views](../modules/saved_views.md) | — |
| `delete_saved_view` | type_reference | [saved_views](../modules/saved_views.md) | — |

> References: showing 12 of 43 logical references; 31 omitted by the 12-row generated summary limit.
