# Project

**Location:** `backend/app/models/project.py:103`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_project](../modules/models_project.md)

## Description

Outcome-oriented planning container above tasks and iterations.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=True)` | — |
| `name` | `Mapped[str]` | `mapped_column(String(255), nullable=False)` | — |
| `timezone` | `Mapped[str]` | `mapped_column(String(64), default='UTC', server_default='UTC', nullable=False)` | — |
| `description` | `Mapped[Optional[str]]` | `mapped_column(Text, nullable=True)` | — |
| `status` | `Mapped[str]` | `mapped_column(String(50), default=ProjectStatus.PLANNED.value, nullable=False, index=True)` | — |
| `health` | `Mapped[str]` | `mapped_column(String(50), default=ProjectHealth.UNKNOWN.value, nullable=False, index=True)` | — |
| `start_date` | `Mapped[Optional[date]]` | `mapped_column(Date, nullable=True)` | — |
| `target_date` | `Mapped[Optional[date]]` | `mapped_column(Date, nullable=True, index=True)` | — |
| `completed_at` | `Mapped[Optional[datetime]]` | `mapped_column(UTCDateTime(), nullable=True)` | — |
| `sort_order` | `Mapped[int]` | `mapped_column(Integer, default=0, nullable=False)` | — |
| `created_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, nullable=False)` | — |
| `updated_at` | `Mapped[datetime]` | `mapped_column(UTCDateTime(), default=utc_now, onupdate=utc_now, nullable=False)` | — |
| `owner_id` | `Mapped[Optional[int]]` | `mapped_column(Integer, ForeignKey('team_members.id', ondelete='SET NULL'), nullable=True, index=True)` | — |
| `owner_profile_id` | `Mapped[Optional[int]]` | `mapped_column(Integer, ForeignKey('team_member_profiles.id', ondelete='SET NULL'), nullable=True, index=True)` | — |
| `initiative_id` | `Mapped[Optional[int]]` | `mapped_column(Integer, ForeignKey('initiatives.id', ondelete='SET NULL'), nullable=True, index=True)` | — |
| `owner` | `Mapped[Optional['TeamMember']]` | `relationship('TeamMember', back_populates='owned_projects')` | — |
| `owner_profile` | `Mapped[Optional['TeamMemberProfile']]` | `relationship('TeamMemberProfile', back_populates='owned_projects')` | — |
| `initiative` | `Mapped[Optional['Initiative']]` | `relationship('Initiative', back_populates='projects')` | — |
| `iterations` | `Mapped[list['Iteration']]` | `relationship('Iteration', back_populates='project', passive_deletes=True)` | — |
| `tasks` | `Mapped[list['Task']]` | `relationship('Task', back_populates='project')` | — |
| `updates` | `Mapped[list['ProjectUpdateEntry']]` | `relationship('ProjectUpdateEntry', back_populates='project', cascade='all, delete-orphan', passive_deletes=True)` | — |
| `milestones` | `Mapped[list['ProjectMilestone']]` | `relationship('ProjectMilestone', back_populates='project', cascade='all, delete-orphan', passive_deletes=True, order_by='ProjectMilestone.sort_order, ProjectMilestone.target_date, ProjectMilestone.id')` | — |
| `releases` | `Mapped[list['Release']]` | `relationship('Release', back_populates='project', cascade='all, delete-orphan', passive_deletes=True, order_by=lambda: [Release.target_date.is_(None), Release.target_date, Release.id])` | — |
| `request_source_links` | `Mapped[list['RequestSourceLink']]` | `relationship('RequestSourceLink', back_populates='project', passive_deletes=True, order_by='RequestSourceLink.created_at, RequestSourceLink.id')` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Project (backend/app/models/project.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/commands.py"]
    n3["backend/app/models/__init__.py"]
    n4["backend/app/models/iteration.py"]
    n5["backend/app/models/release.py"]
    n6["backend/app/models/request_source.py"]
    n7["backend/app/models/task.py"]
    n8["backend/app/models/team_member.py"]
    n9["backend/app/models/triage.py"]
    n10["backend/app/routers/identity.py"]
    n11["AgentWorkService.create_project_update (backend/app/services/agent_work_service.py)"]
    n12["IterationService._response_project (backend/app/services/iteration_service.py)"]
    n13["ProjectService._aggregated_milestone_groups (backend/app/services/project_service.py)"]
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
    click n0 "../modules/models_project.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/commands.md"
    click n3 "../modules/models___init__.md"
    click n4 "../modules/models_iteration.md"
    click n5 "../modules/models_release.md"
    click n6 "../modules/models_request_source.md"
    click n7 "../modules/models_task.md"
    click n8 "../modules/team_member.md"
    click n9 "../modules/models_triage.md"
    click n10 "../modules/routers_identity.md"
    click n11 "../modules/agent_work_service.md"
    click n12 "../modules/iteration_service.md"
    click n13 "../modules/project_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_project](../modules/models_project.md) | 0 | `completed_at`, `created_at`, `description`, `health`, `id`, `initiative`, `initiative_id`, `iterations`, `milestones`, `name`, `owner`, `owner_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `commands` | import | [commands](../modules/commands.md) | — |
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `iteration` | import | [models_iteration](../modules/models_iteration.md) | — |
| `release` | import | [models_release](../modules/models_release.md) | — |
| `request_source` | import | [models_request_source](../modules/models_request_source.md) | — |
| `task` | import | [models_task](../modules/models_task.md) | — |
| `team_member` | import | [team_member](../modules/team_member.md) | — |
| `triage` | import | [models_triage](../modules/models_triage.md) | — |
| `identity` | import | [routers_identity](../modules/routers_identity.md) | — |
| `AgentWorkService.create_project_update` | type_reference | [agent_work_service](../modules/agent_work_service.md) | — |
| `IterationService._response_project` | type_reference | [iteration_service](../modules/iteration_service.md) | — |
| `ProjectService._aggregated_milestone_groups` | type_reference | [project_service](../modules/project_service.md) | — |

> References: showing 12 of 42 logical references; 30 omitted by the 12-row generated summary limit.
