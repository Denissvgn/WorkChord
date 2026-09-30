# PlanningInputRevisions

**Location:** `backend/app/schemas/planning_inputs.py:19`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [planning_inputs](../modules/planning_inputs.md)

## Description

_Auto-generated from `PlanningInputRevisions` in `backend/app/schemas/planning_inputs.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `expected_revisions` | `dict[int, PositiveInt]` | `expected_revisions` | No | No | factory: `dict` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["PlanningInputRevisions (backend/app/schemas/planning_inputs.py)"]
    n1["BaseModel"]
    n2["CalendarCreate (backend/app/schemas/calendar.py)"]
    n3["CalendarUpdate (backend/app/schemas/calendar.py)"]
    n4["IterationUpdate (backend/app/schemas/iteration.py)"]
    n5["ProjectUpdate (backend/app/schemas/project.py)"]
    n6["TeamMemberCreate (backend/app/schemas/team.py)"]
    n7["TeamMemberProfileSkillUpdate (backend/app/schemas/team.py)"]
    n8["TeamMemberProfileUpdate (backend/app/schemas/team.py)"]
    n9["TeamMemberUpdate (backend/app/schemas/team.py)"]
    n10["VacationCreate (backend/app/schemas/team.py)"]
    n11["VacationUpdate (backend/app/schemas/team.py)"]
    n12["backend/app/schemas/calendar.py"]
    n13["backend/app/schemas/iteration.py"]
    n14["backend/app/schemas/project.py"]
    n15["backend/app/schemas/team.py"]
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
    n14 --> n0
    n15 --> n0
    click n0 "../modules/planning_inputs.md"
    click n2 "../modules/schemas_calendar.md"
    click n3 "../modules/schemas_calendar.md"
    click n4 "../modules/schemas_iteration.md"
    click n5 "../modules/schemas_project.md"
    click n6 "../modules/schemas_team.md"
    click n7 "../modules/schemas_team.md"
    click n8 "../modules/schemas_team.md"
    click n9 "../modules/schemas_team.md"
    click n10 "../modules/schemas_team.md"
    click n11 "../modules/schemas_team.md"
    click n12 "../modules/schemas_calendar.md"
    click n13 "../modules/schemas_iteration.md"
    click n14 "../modules/schemas_project.md"
    click n15 "../modules/schemas_team.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [planning_inputs](../modules/planning_inputs.md) | 0 | `expected_revisions` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
| Subclass | `CalendarCreate` | [schemas_calendar](../modules/schemas_calendar.md) |
| Subclass | `CalendarUpdate` | [schemas_calendar](../modules/schemas_calendar.md) |
| Subclass | `IterationUpdate` | [schemas_iteration](../modules/schemas_iteration.md) |
| Subclass | `ProjectUpdate` | [schemas_project](../modules/schemas_project.md) |
| Subclass | `TeamMemberCreate` | [schemas_team](../modules/schemas_team.md) |
| Subclass | `TeamMemberProfileSkillUpdate` | [schemas_team](../modules/schemas_team.md) |
| Subclass | `TeamMemberProfileUpdate` | [schemas_team](../modules/schemas_team.md) |
| Subclass | `TeamMemberUpdate` | [schemas_team](../modules/schemas_team.md) |
| Subclass | `VacationCreate` | [schemas_team](../modules/schemas_team.md) |
| Subclass | `VacationUpdate` | [schemas_team](../modules/schemas_team.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `calendar` | import | [schemas_calendar](../modules/schemas_calendar.md) | — |
| `iteration` | import | [schemas_iteration](../modules/schemas_iteration.md) | — |
| `project` | import | [schemas_project](../modules/schemas_project.md) | — |
| `team` | import | [schemas_team](../modules/schemas_team.md) | — |
