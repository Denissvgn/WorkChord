# VacationImportResponse

**Location:** `backend/app/schemas/team.py:68`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_team](../modules/schemas_team.md)

## Description

Summary of bulk vacation import results.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `imported_count` | `int` | `imported_count` | Yes | No | — | — | — | — |
| `skipped_count` | `int` | `skipped_count` | Yes | No | — | — | — | — |
| `errors` | `list[VacationImportError]` | `errors` | No | No | factory: `list` | — | — | — |
| `vacations` | `list[VacationResponse]` | `vacations` | No | No | factory: `list` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["VacationImportResponse (backend/app/schemas/team.py)"]
    n1["BaseModel"]
    n2["import_team_vacations (backend/app/routers/team.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["TeamService.import_vacations (backend/app/services/team_service.py)"]
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
| [schemas_team](../modules/schemas_team.md) | 0 | `errors`, `imported_count`, `skipped_count`, `vacations` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `import_team_vacations` | type_reference | [routers_team](../modules/routers_team.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `TeamService.import_vacations` | call | [team_service](../modules/team_service.md) | 1 |
| `TeamService.import_vacations` | type_reference | [team_service](../modules/team_service.md) | — |
