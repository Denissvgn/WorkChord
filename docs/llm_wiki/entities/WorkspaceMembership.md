# WorkspaceMembership

**Location:** `backend/app/models/identity.py:33`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_identity](../modules/models_identity.md)

## Description

_Auto-generated from `WorkspaceMembership` in `backend/app/models/identity.py`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `principal_id` | `Mapped[int]` | `mapped_column(ForeignKey('principals.id', ondelete='CASCADE'), primary_key=True)` | — |
| `role` | `Mapped[str]` | `mapped_column(String(16), nullable=False)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WorkspaceMembership (backend/app/models/identity.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["bootstrap (backend/app/routers/identity.py)"]
    n4["workspace_member (backend/app/routers/identity.py)"]
    n5["backend/app/routers/task_domain.py"]
    n6["backend/app/services/discussion_service.py"]
    n7["backend/app/services/identity_service.py"]
    n8["backend/app/services/task_domain_service.py"]
    n9["test_fresh_apply_replay_onboarding_and_runtime_readiness (backend/tests/test_agent_team_setup.py)"]
    n10["test_shared_iteration_snapshots_cannot_reveal_another_project (backend/tests/test_identity_lifecycle.py)"]
    n11["create_empty_project_as_owner (backend/tests/test_managed_authority.py)"]
    n12["test_project_deletion_refuses_live_assignment_scope_without_partial_detach (backend/tests/test_managed_authority.py)"]
    n13["test_workspace_owner_deletes_empty_project_with_retained_audit (backend/tests/test_managed_authority.py)"]
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
    click n4 "../modules/routers_identity.md"
    click n5 "../modules/routers_task_domain.md"
    click n6 "../modules/discussion_service.md"
    click n7 "../modules/identity_service.md"
    click n8 "../modules/task_domain_service.md"
    click n9 "../modules/test_agent_team_setup.md"
    click n10 "../modules/test_identity_lifecycle.md"
    click n11 "../modules/test_managed_authority.md"
    click n12 "../modules/test_managed_authority.md"
    click n13 "../modules/test_managed_authority.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_identity](../modules/models_identity.md) | 0 | `created_at`, `principal_id`, `role` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `bootstrap` | call | [routers_identity](../modules/routers_identity.md) | 1 |
| `workspace_member` | call | [routers_identity](../modules/routers_identity.md) | 1 |
| `task_domain` | import | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `discussion_service` | import | [discussion_service](../modules/discussion_service.md) | — |
| `identity_service` | import | [identity_service](../modules/identity_service.md) | — |
| `task_domain_service` | import | [task_domain_service](../modules/task_domain_service.md) | — |
| `test_fresh_apply_replay_onboarding_and_runtime_readiness` | call | [test_agent_team_setup](../modules/test_agent_team_setup.md) | 1 |
| `test_shared_iteration_snapshots_cannot_reveal_another_project` | call | [test_identity_lifecycle](../modules/test_identity_lifecycle.md) | 1 |
| `create_empty_project_as_owner` | call | [test_managed_authority](../modules/test_managed_authority.md) | 1 |
| `test_project_deletion_refuses_live_assignment_scope_without_partial_detach` | call | [test_managed_authority](../modules/test_managed_authority.md) | 1 |
| `test_workspace_owner_deletes_empty_project_with_retained_audit` | call | [test_managed_authority](../modules/test_managed_authority.md) | 1 |

> References: showing 12 of 14 logical references; 2 omitted by the 12-row generated summary limit.
