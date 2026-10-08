# ProjectMembership

**Location:** `backend/app/models/identity.py:49`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_identity](../modules/models_identity.md)

## Description

_Auto-generated from `ProjectMembership` in `backend/app/models/identity.py`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `principal_id` | `Mapped[int]` | `mapped_column(ForeignKey('principals.id', ondelete='CASCADE'), primary_key=True)` | — |
| `project_id` | `Mapped[int]` | `mapped_column(ForeignKey('projects.id', ondelete='CASCADE'), primary_key=True)` | — |
| `role` | `Mapped[str]` | `mapped_column(String(16), nullable=False)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProjectMembership (backend/app/models/identity.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["project_member (backend/app/routers/identity.py)"]
    n4["backend/app/routers/task_domain.py"]
    n5["backend/app/services/discussion_service.py"]
    n6["backend/app/services/identity_service.py"]
    n7["backend/app/services/task_domain_service.py"]
    n8["backend/tests/migrations/test_project_identity.py"]
    n9["managed_store (backend/tests/test_managed_authority.py)"]
    n10["backend/tests/test_task_discussion.py"]
    n11["human_context (backend/tests/test_task_domain.py)"]
    n12["_source_phase (scripts/ci/installed_wheel_postgresql_qualification.py)"]
    n13["scripts/ci/serve_disposable_api.py"]
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
    click n0 "../modules/models_identity.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/routers_identity.md"
    click n4 "../modules/routers_task_domain.md"
    click n5 "../modules/discussion_service.md"
    click n6 "../modules/identity_service.md"
    click n7 "../modules/task_domain_service.md"
    click n8 "../modules/test_project_identity.md"
    click n9 "../modules/test_managed_authority.md"
    click n10 "../modules/test_task_discussion.md"
    click n11 "../modules/test_task_domain.md"
    click n12 "../modules/installed_wheel_postgresql_qualification.md"
    click n13 "../modules/serve_disposable_api.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_identity](../modules/models_identity.md) | 0 | `created_at`, `principal_id`, `project_id`, `role` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `project_member` | call | [routers_identity](../modules/routers_identity.md) | 1 |
| `task_domain` | import | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `discussion_service` | import | [discussion_service](../modules/discussion_service.md) | — |
| `identity_service` | import | [identity_service](../modules/identity_service.md) | — |
| `task_domain_service` | import | [task_domain_service](../modules/task_domain_service.md) | — |
| `test_project_identity` | import | [test_project_identity](../modules/test_project_identity.md) | — |
| `managed_store` | call | [test_managed_authority](../modules/test_managed_authority.md) | 2 |
| `test_task_discussion` | import | [test_task_discussion](../modules/test_task_discussion.md) | — |
| `human_context` | call | [test_task_domain](../modules/test_task_domain.md) | 2 |
| `_source_phase` | call | [installed_wheel_postgresql_qualification](../modules/installed_wheel_postgresql_qualification.md) | 1 |
| `serve_disposable_api` | import | [serve_disposable_api](../modules/serve_disposable_api.md) | — |
