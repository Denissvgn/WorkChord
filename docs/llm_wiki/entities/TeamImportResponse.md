# TeamImportResponse

**Location:** `backend/app/schemas/team.py:346`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_team](../modules/schemas_team.md)

## Description

Response for team import.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `imported_count` | `int` | `imported_count` | Yes | No | — | — | — | — |
| `members` | `list[TeamMemberResponse]` | `members` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TeamImportResponse (backend/app/schemas/team.py)"]
    n1["BaseModel"]
    n2["import_team_members (backend/app/routers/team.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_team.md"
    click n2 "../modules/routers_team.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_team](../modules/schemas_team.md) | 0 | `imported_count`, `members` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `import_team_members` | call | [routers_team](../modules/routers_team.md) | 1 |
| `import_team_members` | type_reference | [routers_team](../modules/routers_team.md) | — |
