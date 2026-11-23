# TeamMemberProfileCompact

**Location:** `backend/app/schemas/team.py:271`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_team](../modules/schemas_team.md)

## Description

Compact profile data embedded in team-member responses.

A reader who may read the team row but not the profile itself gets the id, display name,
kind, automation flag, assignment modes and agent_connected; email, headline and skills
are then null or empty.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `from_attributes` | `True` | model_config |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `id` | `int` | `id` | Yes | No | — | — | — | — |
| `display_name` | `str` | `display_name` | Yes | No | — | — | — | — |
| `email` | `Optional[str]` | `email` | No | Yes | `None` | — | — | — |
| `headline` | `Optional[str]` | `headline` | No | Yes | `None` | — | — | — |
| `automation_enabled` | `bool` | `automation_enabled` | Yes | No | — | — | — | — |
| `profile_kind` | `str` | `profile_kind` | No | No | `'human'` | — | — | — |
| `assignment_modes` | `list[str]` | `assignment_modes` | No | No | factory: `list` | — | — | — |
| `skills` | `list[TeamMemberProfileSkillResponse]` | `skills` | No | No | factory: `list` | — | — | — |
| `agent_connected` | `bool` | `agent_connected` | No | No | `False` | — | — | True when an enabled agent is bound to this profile. Read-only; names no agent. |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TeamMemberProfileCompact (backend/app/schemas/team.py)"]
    n1["BaseModel"]
    n2["backend/app/schemas/__init__.py"]
    n3["backend/app/schemas/project.py"]
    n4["backend/app/services/project_service.py"]
    n5["TeamService._attach_assignee_profiles (backend/app/services/team_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/schemas_team.md"
    click n2 "../modules/schemas___init__.md"
    click n3 "../modules/schemas_project.md"
    click n4 "../modules/project_service.md"
    click n5 "../modules/team_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_team](../modules/schemas_team.md) | 0 | `agent_connected`, `assignment_modes`, `automation_enabled`, `display_name`, `email`, `headline`, `id`, `profile_kind`, `skills` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `project` | import | [schemas_project](../modules/schemas_project.md) | — |
| `project_service` | import | [project_service](../modules/project_service.md) | — |
| `TeamService._attach_assignee_profiles` | call | [team_service](../modules/team_service.md) | 1 |
