# calendar Module

**Path:** `backend/app/models/calendar.py`

## Description

Calendar model.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.models.iteration` | `Iteration` |
| `datetime` | `date` |
| `sqlalchemy` | `JSON`, `Float`, `Integer`, `String` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column`, `relationship` |
| `typing` | `TYPE_CHECKING` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/models/calendar.py"]
    n2["scripts"]
    n0 --> n1
    n1 --> n0
    n2 --> n1
    click n1 "../modules/models_calendar.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (23) |
| Inbound | `scripts` (1) |
| Outbound | `backend` (2) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 25 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [Calendar](../entities/models_calendar_Calendar.md) | 14 | `Base` | Production calendar model. |
