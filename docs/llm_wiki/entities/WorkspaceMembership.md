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
    n5["backend/app/services/identity_service.py"]
    n6["test_fresh_apply_replay_onboarding_and_runtime_readiness (backend/tests/test_agent_team_setup.py)"]
    n7["test_shared_iteration_snapshots_cannot_reveal_another_project (backend/tests/test_identity_lifecycle.py)"]
    n8["backend/tests/test_managed_authority.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/models_identity.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/routers_identity.md"
    click n4 "../modules/routers_identity.md"
    click n5 "../modules/identity_service.md"
    click n6 "../modules/test_agent_team_setup.md"
    click n7 "../modules/test_identity_lifecycle.md"
    click n8 "../modules/test_managed_authority.md"
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
| `identity_service` | import | [identity_service](../modules/identity_service.md) | — |
| `test_fresh_apply_replay_onboarding_and_runtime_readiness` | call | [test_agent_team_setup](../modules/test_agent_team_setup.md) | 1 |
| `test_shared_iteration_snapshots_cannot_reveal_another_project` | call | [test_identity_lifecycle](../modules/test_identity_lifecycle.md) | 1 |
| `test_managed_authority` | import | [test_managed_authority](../modules/test_managed_authority.md) | — |
