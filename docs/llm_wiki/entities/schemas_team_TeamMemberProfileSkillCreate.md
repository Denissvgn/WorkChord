# TeamMemberProfileSkillCreate

**Location:** `backend/app/schemas/team.py:100`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_team](../modules/schemas_team.md)

## Description

Schema for creating a profile skill or weakness.

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `trim_required_text` | field | skill_key, skill_name | after | — |
| `trim_optional_text` | field | category, notes | after | — |
| `validate_keywords` | field | keywords_json | before | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `skill_key` | `str` | `skill_key` | Yes | No | — | max_length=120; min_length=1 | — | — |
| `skill_name` | `str` | `skill_name` | Yes | No | — | max_length=255; min_length=1 | — | — |
| `category` | `Optional[str]` | `category` | No | Yes | `None` | max_length=120 | — | — |
| `level` | `int` | `level` | No | No | `3` | ge=1; le=5 | — | — |
| `interest` | `int` | `interest` | No | No | `3` | ge=1; le=5 | — | — |
| `is_weakness` | `bool` | `is_weakness` | No | No | `False` | — | — | — |
| `keywords_json` | `list[str]` | `keywords_json` | No | No | factory: `list` | — | — | — |
| `notes` | `Optional[str]` | `notes` | No | Yes | `None` | — | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `trim_required_text` | `(value: str) -> str` | `@field_validator('skill_key', 'skill_name', mode='after')`, `@classmethod` | — |
| `trim_optional_text` | `(value: Optional[str]) -> Optional[str]` | `@field_validator('category', 'notes', mode='after')`, `@classmethod` | — |
| `validate_keywords` | `(value: Any) -> list[str]` | `@field_validator('keywords_json', mode='before')`, `@classmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TeamMemberProfileSkillCreate (backend/app/schemas/team.py)"]
    n1["BaseModel"]
    n2["create_team_member_profile_skill (backend/app/routers/team.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["TeamService.add_profile_skill (backend/app/services/team_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_team.md"
    click n2 "../modules/routers_team.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/team_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_team](../modules/schemas_team.md) | 3 | `category`, `interest`, `is_weakness`, `keywords_json`, `level`, `notes`, `skill_key`, `skill_name` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_team_member_profile_skill` | type_reference | [routers_team](../modules/routers_team.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `TeamService.add_profile_skill` | type_reference | [team_service](../modules/team_service.md) | — |
