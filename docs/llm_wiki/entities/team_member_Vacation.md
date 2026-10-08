# Vacation

**Location:** `backend/app/models/team_member.py:164`
**Kind:** Class
**Bases:** `Base`
**Module:** [team_member](../modules/team_member.md)

## Description

Vacation period for a team member.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=True)` | — |
| `start_date` | `Mapped[date]` | `mapped_column(Date, nullable=False)` | — |
| `end_date` | `Mapped[date]` | `mapped_column(Date, nullable=False)` | — |
| `team_member_id` | `Mapped[int]` | `mapped_column(Integer, ForeignKey('team_members.id'), nullable=False)` | — |
| `profile_absence_id` | `Mapped[int \| None]` | `mapped_column(ForeignKey('profile_absences.id', ondelete='RESTRICT'), nullable=True, index=True)` | — |
| `team_member` | `Mapped['TeamMember']` | `relationship('TeamMember', back_populates='vacations')` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Vacation (backend/app/models/team_member.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["AgentPlanningService.create_vacation (backend/app/services/agent_planning_service.py)"]
    n4["AgentPlanningService.update_vacation (backend/app/services/agent_planning_service.py)"]
    n5["backend/app/services/capacity_service.py"]
    n6["backend/app/services/planning_input_context.py"]
    n7["backend/app/services/scheduler_service.py"]
    n8["SnapshotService.restore (backend/app/services/snapshot_service.py)"]
    n9["TeamService.add_vacation (backend/app/services/team_service.py)"]
    n10["TeamService.import_vacations (backend/app/services/team_service.py)"]
    n11["TeamService.update_vacation (backend/app/services/team_service.py)"]
    n12["test_context_covers_each_shared_resource_and_new_member_target (backend/tests/test_planning_input_context.py)"]
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
    click n3 "../modules/agent_planning_service.md"
    click n4 "../modules/agent_planning_service.md"
    click n5 "../modules/capacity_service.md"
    click n6 "../modules/planning_input_context.md"
    click n7 "../modules/scheduler_service.md"
    click n8 "../modules/snapshot_service.md"
    click n9 "../modules/team_service.md"
    click n10 "../modules/team_service.md"
    click n11 "../modules/team_service.md"
    click n12 "../modules/test_planning_input_context.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [team_member](../modules/team_member.md) | 0 | `end_date`, `id`, `profile_absence_id`, `start_date`, `team_member`, `team_member_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `AgentPlanningService.create_vacation` | type_reference | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `AgentPlanningService.update_vacation` | type_reference | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `capacity_service` | import | [capacity_service](../modules/capacity_service.md) | — |
| `planning_input_context` | import | [planning_input_context](../modules/planning_input_context.md) | — |
| `scheduler_service` | import | [scheduler_service](../modules/scheduler_service.md) | — |
| `SnapshotService.restore` | call | [snapshot_service](../modules/snapshot_service.md) | 1 |
| `TeamService.add_vacation` | call | [team_service](../modules/team_service.md) | 1 |
| `TeamService.add_vacation` | type_reference | [team_service](../modules/team_service.md) | — |
| `TeamService.import_vacations` | type_reference | [team_service](../modules/team_service.md) | — |
| `TeamService.update_vacation` | type_reference | [team_service](../modules/team_service.md) | — |
| `test_context_covers_each_shared_resource_and_new_member_target` | call | [test_planning_input_context](../modules/test_planning_input_context.md) | 1 |

> References: showing 12 of 16 logical references; 4 omitted by the 12-row generated summary limit.
