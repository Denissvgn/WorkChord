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

*No declared methods.*

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
    n7["backend/app/services/execution_planning_window.py"]
    n8["backend/app/services/identity_service.py"]
    n9["backend/app/services/review_evidence.py"]
    n10["backend/app/services/task_domain_service.py"]
    n11["test_binding_and_preset_routes_preserve_credential_permissions (backend/tests/test_agent_model_catalog_api.py)"]
    n12["test_model_catalog_routes_accept_admin_key_agent_key_and_refuse_neither (backend/tests/test_agent_model_catalog_api.py)"]
    n13["test_fresh_apply_replay_onboarding_and_runtime_readiness (backend/tests/test_agent_team_setup.py)"]
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
    click n7 "../modules/execution_planning_window.md"
    click n8 "../modules/identity_service.md"
    click n9 "../modules/services_review_evidence.md"
    click n10 "../modules/task_domain_service.md"
    click n11 "../modules/test_agent_model_catalog_api.md"
    click n12 "../modules/test_agent_model_catalog_api.md"
    click n13 "../modules/test_agent_team_setup.md"
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
| `execution_planning_window` | import | [execution_planning_window](../modules/execution_planning_window.md) | — |
| `identity_service` | import | [identity_service](../modules/identity_service.md) | — |
| `review_evidence` | import | [services_review_evidence](../modules/services_review_evidence.md) | — |
| `task_domain_service` | import | [task_domain_service](../modules/task_domain_service.md) | — |
| `test_binding_and_preset_routes_preserve_credential_permissions` | call | [test_agent_model_catalog_api](../modules/test_agent_model_catalog_api.md) | 1 |
| `test_model_catalog_routes_accept_admin_key_agent_key_and_refuse_neither` | call | [test_agent_model_catalog_api](../modules/test_agent_model_catalog_api.md) | 1 |
| `test_fresh_apply_replay_onboarding_and_runtime_readiness` | call | [test_agent_team_setup](../modules/test_agent_team_setup.md) | 1 |

> References: showing 12 of 44 logical references; 32 omitted by the 12-row generated summary limit.
