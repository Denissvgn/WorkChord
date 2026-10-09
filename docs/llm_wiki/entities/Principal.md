# Principal

**Location:** `backend/app/models/identity.py:12`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_identity](../modules/models_identity.md)

## Description

_Auto-generated from `Principal` in `backend/app/models/identity.py`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True)` | — |
| `kind` | `Mapped[str]` | `mapped_column(String(16), nullable=False)` | — |
| `display_name` | `Mapped[str]` | `mapped_column(String(255), nullable=False)` | — |
| `enabled` | `Mapped[bool]` | `mapped_column(Boolean, default=True, nullable=False)` | — |
| `agent_actor_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('agent_actors.id', ondelete='RESTRICT'), unique=True)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Principal (backend/app/models/identity.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/http_authority.py"]
    n3["backend/app/models/__init__.py"]
    n4["backend/app/models/user_session.py"]
    n5["recover_principal (backend/app/routers/identity.py)"]
    n6["backend/app/routers/task_domain.py"]
    n7["AgentService.create_actor (backend/app/services/agent_service.py)"]
    n8["AgentTeamSetupService.acknowledge_runtime (backend/app/services/agent_team_setup_service.py)"]
    n9["backend/app/services/discussion_service.py"]
    n10["IdentityService.actor_context (backend/app/services/identity_service.py)"]
    n11["IdentityService.context (backend/app/services/identity_service.py)"]
    n12["IdentityService.finish_login (backend/app/services/identity_service.py)"]
    n13["initialize_control_plane (backend/app/services/identity_service.py)"]
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
    click n2 "../modules/http_authority.md"
    click n3 "../modules/models___init__.md"
    click n4 "../modules/user_session.md"
    click n5 "../modules/routers_identity.md"
    click n6 "../modules/routers_task_domain.md"
    click n7 "../modules/agent_service.md"
    click n8 "../modules/agent_team_setup_service.md"
    click n9 "../modules/discussion_service.md"
    click n10 "../modules/identity_service.md"
    click n11 "../modules/identity_service.md"
    click n12 "../modules/identity_service.md"
    click n13 "../modules/identity_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_identity](../modules/models_identity.md) | 0 | `agent_actor_id`, `created_at`, `display_name`, `enabled`, `id`, `kind` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `http_authority` | import | [http_authority](../modules/http_authority.md) | — |
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `user_session` | import | [user_session](../modules/user_session.md) | — |
| `recover_principal` | type_reference | [routers_identity](../modules/routers_identity.md) | — |
| `task_domain` | import | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `AgentService.create_actor` | call | [agent_service](../modules/agent_service.md) | 1 |
| `AgentTeamSetupService.acknowledge_runtime` | call | [agent_team_setup_service](../modules/agent_team_setup_service.md) | 1 |
| `discussion_service` | import | [discussion_service](../modules/discussion_service.md) | — |
| `IdentityService.actor_context` | call | [identity_service](../modules/identity_service.md) | 1 |
| `IdentityService.context` | type_reference | [identity_service](../modules/identity_service.md) | — |
| `IdentityService.finish_login` | call | [identity_service](../modules/identity_service.md) | 1 |
| `initialize_control_plane` | call | [identity_service](../modules/identity_service.md) | 1 |

> References: showing 12 of 31 logical references; 19 omitted by the 12-row generated summary limit.
