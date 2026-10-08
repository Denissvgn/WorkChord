# CommandAudit

**Location:** `backend/app/models/identity.py:86`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_identity](../modules/models_identity.md)

## Description

_Auto-generated from `CommandAudit` in `backend/app/models/identity.py`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True)` | — |
| `principal_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('principals.id', ondelete='RESTRICT'), index=True)` | — |
| `project_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('projects.id', ondelete='SET NULL'), index=True)` | — |
| `action` | `Mapped[str]` | `mapped_column(String(128), nullable=False)` | — |
| `source` | `Mapped[str]` | `mapped_column(String(32), nullable=False)` | — |
| `correlation_id` | `Mapped[str]` | `mapped_column(String(128), nullable=False)` | — |
| `reason` | `Mapped[str \| None]` | `mapped_column(Text)` | — |
| `details` | `Mapped[dict]` | `mapped_column(JSON, default=dict, nullable=False)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, index=True)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CommandAudit (backend/app/models/identity.py)"]
    n1["Base (backend/app/database.py)"]
    n2["append_command_audit (backend/app/authority.py)"]
    n3["backend/app/models/__init__.py"]
    n4["bootstrap (backend/app/routers/identity.py)"]
    n5["link_profile (backend/app/routers/identity.py)"]
    n6["project_member (backend/app/routers/identity.py)"]
    n7["recover_principal (backend/app/routers/identity.py)"]
    n8["workspace_member (backend/app/routers/identity.py)"]
    n9["IdentityService.transfer_guest (backend/app/services/identity_service.py)"]
    n10["backend/tests/database_migration/test_project_identity_scope.py"]
    n11["backend/tests/migrations/test_project_identity.py"]
    n12["backend/tests/test_managed_authority.py"]
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
    click n0 "../modules/models_identity.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/authority.md"
    click n3 "../modules/models___init__.md"
    click n4 "../modules/routers_identity.md"
    click n5 "../modules/routers_identity.md"
    click n6 "../modules/routers_identity.md"
    click n7 "../modules/routers_identity.md"
    click n8 "../modules/routers_identity.md"
    click n9 "../modules/identity_service.md"
    click n10 "../modules/test_project_identity_scope.md"
    click n11 "../modules/test_project_identity.md"
    click n12 "../modules/test_managed_authority.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_identity](../modules/models_identity.md) | 0 | `action`, `correlation_id`, `created_at`, `details`, `id`, `principal_id`, `project_id`, `reason`, `source` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `append_command_audit` | call | [authority](../modules/authority.md) | 1 |
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `bootstrap` | call | [routers_identity](../modules/routers_identity.md) | 1 |
| `link_profile` | call | [routers_identity](../modules/routers_identity.md) | 1 |
| `project_member` | call | [routers_identity](../modules/routers_identity.md) | 1 |
| `recover_principal` | call | [routers_identity](../modules/routers_identity.md) | 1 |
| `workspace_member` | call | [routers_identity](../modules/routers_identity.md) | 1 |
| `IdentityService.transfer_guest` | call | [identity_service](../modules/identity_service.md) | 1 |
| `test_project_identity_scope` | import | [test_project_identity_scope](../modules/test_project_identity_scope.md) | — |
| `test_project_identity` | import | [test_project_identity](../modules/test_project_identity.md) | — |
| `test_managed_authority` | import | [test_managed_authority](../modules/test_managed_authority.md) | — |
