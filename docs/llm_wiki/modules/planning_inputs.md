# planning_inputs Module

**Path:** `backend/app/schemas/planning_inputs.py`

## Description

Validated working zones and optional aggregate revisions for shared inputs.

## Imports

| Source | Symbols |
|--------|---------|
| `pydantic` | `AfterValidator`, `BaseModel`, `Field`, `PositiveInt` |
| `typing` | `Annotated` |
| `zoneinfo` | `ZoneInfo`, `ZoneInfoNotFoundError` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/schemas/calendar.py"]
    n1["backend/app/schemas/iteration.py"]
    n2["backend/app/schemas/planning_inputs.py"]
    n3["backend/app/schemas/project.py"]
    n4["backend/app/schemas/team.py"]
    n0 --> n2
    n1 --> n2
    n3 --> n2
    n3 --> n4
    n4 --> n2
    click n0 "../modules/schemas_calendar.md"
    click n1 "../modules/schemas_iteration.md"
    click n2 "../modules/planning_inputs.md"
    click n3 "../modules/schemas_project.md"
    click n4 "../modules/schemas_team.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [schemas_calendar](../modules/schemas_calendar.md) |
| Inbound | [schemas_iteration](../modules/schemas_iteration.md) |
| Inbound | [schemas_project](../modules/schemas_project.md) |
| Inbound | [schemas_team](../modules/schemas_team.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [WorkingZone](../entities/WorkingZone.md) | Type alias | 16 | `Annotated[str, AfterValidator(validate_working_zone)]` | — |
| [PlanningInputRevisions](../entities/PlanningInputRevisions.md) | Pydantic model | 19 | `BaseModel` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `validate_working_zone` | `(value: str) -> str` | — | — |
