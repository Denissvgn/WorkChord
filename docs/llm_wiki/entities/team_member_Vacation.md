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
| `team_member` | `Mapped['TeamMember']` | `relationship('TeamMember', back_populates='vacations')` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Vacation (backend/app/models/team_member.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/commands.py"]
    n3["backend/app/models/__init__.py"]
    n4["AgentPlanningService.create_vacation (backend/app/services/agent_planning_service.py)"]
    n5["AgentPlanningService.update_vacation (backend/app/services/agent_planning_service.py)"]
    n6["backend/app/services/scheduler_service.py"]
    n7["SnapshotService.restore (backend/app/services/snapshot_service.py)"]
    n8["TeamService.add_vacation (backend/app/services/team_service.py)"]
    n9["TeamService.import_vacations (backend/app/services/team_service.py)"]
    n10["TeamService.update_vacation (backend/app/services/team_service.py)"]
    n11["test_restore_recovers_dates_and_absences_without_inventing_acceptance (backend/tests/test_work_correctness.py)"]
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
    click n0 "../modules/team_member.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/commands.md"
    click n3 "../modules/models___init__.md"
    click n4 "../modules/agent_planning_service.md"
    click n5 "../modules/agent_planning_service.md"
    click n6 "../modules/scheduler_service.md"
    click n7 "../modules/snapshot_service.md"
    click n8 "../modules/team_service.md"
    click n9 "../modules/team_service.md"
    click n10 "../modules/team_service.md"
    click n11 "../modules/test_work_correctness.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [team_member](../modules/team_member.md) | 0 | `end_date`, `id`, `start_date`, `team_member`, `team_member_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `commands` | import | [commands](../modules/commands.md) | — |
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `AgentPlanningService.create_vacation` | type_reference | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `AgentPlanningService.update_vacation` | type_reference | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `scheduler_service` | import | [scheduler_service](../modules/scheduler_service.md) | — |
| `SnapshotService.restore` | call | [snapshot_service](../modules/snapshot_service.md) | 1 |
| `TeamService.add_vacation` | call | [team_service](../modules/team_service.md) | 1 |
| `TeamService.add_vacation` | type_reference | [team_service](../modules/team_service.md) | — |
| `TeamService.import_vacations` | call | [team_service](../modules/team_service.md) | 1 |
| `TeamService.import_vacations` | type_reference | [team_service](../modules/team_service.md) | — |
| `TeamService.update_vacation` | type_reference | [team_service](../modules/team_service.md) | — |
| `test_restore_recovers_dates_and_absences_without_inventing_acceptance` | call | [test_work_correctness](../modules/test_work_correctness.md) | 1 |
