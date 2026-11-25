# capacity Module

**Path:** `backend/app/models/capacity.py`

## Description

Durable person availability and a serialization point for shared planning.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.models.calendar` | `Calendar`, `profile_annual_calendars` |
| `datetime` | `date` |
| `sqlalchemy` | `CheckConstraint`, `Date`, `ForeignKey`, `Integer`, `JSON`, `String` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column`, `relationship` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/models/capacity.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/models_capacity.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (17) |
| Outbound | `backend` (2) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 19 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [PlanningState](../entities/PlanningState.md) | 12 | `Base` | — |
| [ProfileAvailability](../entities/ProfileAvailability.md) | 20 | `Base` | — |
| [ProfileAbsence](../entities/ProfileAbsence.md) | 34 | `Base` | — |
