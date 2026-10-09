# Iteration

**Location:** `backend/app/models/iteration.py:18`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_iteration](../modules/models_iteration.md)

## Description

Development iteration (sprint) model.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=True)` | — |
| `name` | `Mapped[str]` | `mapped_column(String(255), nullable=False)` | — |
| `revision` | `Mapped[int]` | `mapped_column(Integer, default=1, server_default='1', nullable=False)` | — |
| `start_date` | `Mapped[date]` | `mapped_column(Date, nullable=False)` | — |
| `end_date` | `Mapped[date]` | `mapped_column(Date, nullable=False)` | — |
| `manager_email` | `Mapped[Optional[str]]` | `mapped_column(String(255), nullable=True)` | — |
| `calendar_id` | `Mapped[int]` | `mapped_column(Integer, ForeignKey('calendars.id'), nullable=False)` | — |
| `project_id` | `Mapped[Optional[int]]` | `mapped_column(Integer, ForeignKey('projects.id', ondelete='SET NULL', use_alter=True), nullable=True, index=True)` | — |
| `calendar` | `Mapped['Calendar']` | `relationship('Calendar', back_populates='iterations')` | — |
| `project` | `Mapped[Optional['Project']]` | `relationship('Project', back_populates='iterations')` | — |
| `team_members` | `Mapped[list['TeamMember']]` | `relationship('TeamMember', back_populates='iteration')` | — |
| `tasks` | `Mapped[list['Task']]` | `relationship('Task', back_populates='iteration', cascade='all, delete-orphan')` | — |
| `plan_shares` | `Mapped[list['PlanShare']]` | `relationship('PlanShare', back_populates='iteration', cascade='all, delete-orphan')` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Iteration (backend/app/models/iteration.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/commands.py"]
    n3["backend/app/models/__init__.py"]
    n4["backend/app/models/calendar.py"]
    n5["backend/app/models/plan_share.py"]
    n6["backend/app/models/project.py"]
    n7["backend/app/models/task.py"]
    n8["backend/app/models/team_member.py"]
    n9["backend/app/models/triage.py"]
    n10["backend/app/routers/tasks.py"]
    n11["AgentPlanningService._require_iteration_for_update (backend/app/services/agent_planning_service.py)"]
    n12["AgentPlanningService.create_iteration (backend/app/services/agent_planning_service.py)"]
    n13["AgentPlanningService.update_iteration (backend/app/services/agent_planning_service.py)"]
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
    click n0 "../modules/models_iteration.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/commands.md"
    click n3 "../modules/models___init__.md"
    click n4 "../modules/models_calendar.md"
    click n5 "../modules/models_plan_share.md"
    click n6 "../modules/models_project.md"
    click n7 "../modules/models_task.md"
    click n8 "../modules/team_member.md"
    click n9 "../modules/models_triage.md"
    click n10 "../modules/tasks.md"
    click n11 "../modules/agent_planning_service.md"
    click n12 "../modules/agent_planning_service.md"
    click n13 "../modules/agent_planning_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_iteration](../modules/models_iteration.md) | 0 | `calendar`, `calendar_id`, `end_date`, `id`, `manager_email`, `name`, `plan_shares`, `project`, `project_id`, `revision`, `start_date`, `tasks` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `commands` | import | [commands](../modules/commands.md) | — |
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `calendar` | import | [models_calendar](../modules/models_calendar.md) | — |
| `plan_share` | import | [models_plan_share](../modules/models_plan_share.md) | — |
| `project` | import | [models_project](../modules/models_project.md) | — |
| `task` | import | [models_task](../modules/models_task.md) | — |
| `team_member` | import | [team_member](../modules/team_member.md) | — |
| `triage` | import | [models_triage](../modules/models_triage.md) | — |
| `tasks` | import | [tasks](../modules/tasks.md) | — |
| `AgentPlanningService._require_iteration_for_update` | type_reference | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `AgentPlanningService.create_iteration` | type_reference | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `AgentPlanningService.update_iteration` | type_reference | [agent_planning_service](../modules/agent_planning_service.md) | — |

> References: showing 12 of 82 logical references; 70 omitted by the 12-row generated summary limit.
