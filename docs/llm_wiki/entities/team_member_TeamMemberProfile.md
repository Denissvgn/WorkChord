# TeamMemberProfile

**Location:** `backend/app/models/team_member.py:71`
**Kind:** Class
**Bases:** `Base`
**Module:** [team_member](../modules/team_member.md)

## Description

Reusable person profile for durable capability and preference metadata.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=True)` | — |
| `profile_token` | `Mapped[str]` | `mapped_column(String(36), nullable=False, default=lambda: str(uuid4()))` | — |
| `seed_key` | `Mapped[Optional[str]]` | `mapped_column(String(120), nullable=True, unique=True, index=True)` | — |
| `display_name` | `Mapped[str]` | `mapped_column(String(255), nullable=False)` | — |
| `email` | `Mapped[Optional[str]]` | `mapped_column(String(255), nullable=True)` | — |
| `headline` | `Mapped[Optional[str]]` | `mapped_column(String(255), nullable=True)` | — |
| `summary` | `Mapped[Optional[str]]` | `mapped_column(Text, nullable=True)` | — |
| `notes` | `Mapped[Optional[str]]` | `mapped_column(Text, nullable=True)` | — |
| `automation_enabled` | `Mapped[bool]` | `mapped_column(Boolean, default=True, nullable=False)` | — |
| `profile_kind` | `Mapped[str]` | `mapped_column(String(30), default='human', nullable=False)` | — |
| `assignment_modes` | `Mapped[list[Any]]` | `mapped_column(JSON, default=list, nullable=False)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, nullable=False)` | — |
| `updated_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False)` | — |
| `skills` | `Mapped[list['TeamMemberProfileSkill']]` | `relationship('TeamMemberProfileSkill', back_populates='profile', cascade='all, delete-orphan', order_by='TeamMemberProfileSkill.category, TeamMemberProfileSkill.skill_name, TeamMemberProfileSkill.id')` | — |
| `team_members` | `Mapped[list['TeamMember']]` | `relationship('TeamMember', back_populates='profile', passive_deletes=True)` | — |
| `agent_actors` | `Mapped[list['AgentActor']]` | `relationship('AgentActor', back_populates='profile', passive_deletes=True)` | — |
| `owned_projects` | `Mapped[list['Project']]` | `relationship('Project', back_populates='owner_profile', passive_deletes=True)` | — |
| `owned_initiatives` | `Mapped[list['Initiative']]` | `relationship('Initiative', back_populates='owner_profile', passive_deletes=True)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TeamMemberProfile (backend/app/models/team_member.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["backend/app/models/agent.py"]
    n4["backend/app/models/project.py"]
    n5["backend/app/models/task.py"]
    n6["backend/app/routers/agent.py"]
    n7["backend/app/routers/identity.py"]
    n8["backend/app/routers/task_domain.py"]
    n9["AgentProfileCatalogService.apply_preset (backend/app/services/agent_profile_catalog_service.py)"]
    n10["AgentRoutingService._profile_evidence (backend/app/services/agent_routing_service.py)"]
    n11["AgentRoutingService._profile_revision (backend/app/services/agent_routing_service.py)"]
    n12["backend/app/services/agent_service.py"]
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
    click n0 "../modules/team_member.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/models_agent.md"
    click n4 "../modules/models_project.md"
    click n5 "../modules/models_task.md"
    click n6 "../modules/routers_agent.md"
    click n7 "../modules/routers_identity.md"
    click n8 "../modules/routers_task_domain.md"
    click n9 "../modules/agent_profile_catalog_service.md"
    click n10 "../modules/agent_routing_service.md"
    click n11 "../modules/agent_routing_service.md"
    click n12 "../modules/agent_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [team_member](../modules/team_member.md) | 0 | `agent_actors`, `assignment_modes`, `automation_enabled`, `created_at`, `display_name`, `email`, `headline`, `id`, `notes`, `owned_initiatives`, `owned_projects`, `profile_kind` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `agent` | import | [models_agent](../modules/models_agent.md) | — |
| `project` | import | [models_project](../modules/models_project.md) | — |
| `task` | import | [models_task](../modules/models_task.md) | — |
| `agent` | import | [routers_agent](../modules/routers_agent.md) | — |
| `identity` | import | [routers_identity](../modules/routers_identity.md) | — |
| `task_domain` | import | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `AgentProfileCatalogService.apply_preset` | call | [agent_profile_catalog_service](../modules/agent_profile_catalog_service.md) | 1 |
| `AgentProfileCatalogService.apply_preset` | type_reference | [agent_profile_catalog_service](../modules/agent_profile_catalog_service.md) | — |
| `AgentRoutingService._profile_evidence` | type_reference | [agent_routing_service](../modules/agent_routing_service.md) | — |
| `AgentRoutingService._profile_revision` | type_reference | [agent_routing_service](../modules/agent_routing_service.md) | — |
| `agent_service` | import | [agent_service](../modules/agent_service.md) | — |

> References: showing 12 of 70 logical references; 58 omitted by the 12-row generated summary limit.
