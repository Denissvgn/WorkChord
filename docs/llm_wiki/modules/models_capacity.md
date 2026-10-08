# capacity Module

**Path:** `backend/app/models/capacity.py`

## Description

Durable person availability and a serialization point for shared planning.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `datetime` | `date` |
| `sqlalchemy` | `CheckConstraint`, `Date`, `ForeignKey`, `Integer`, `JSON`, `String` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/commands.py"]
    n1["backend/app/database.py"]
    n2["backend/app/models/__init__.py"]
    n3["backend/app/models/capacity.py"]
    n4["backend/app/services/capacity_service.py"]
    n5["backend/app/services/planning_input_context.py"]
    n6["backend/tests/test_planning_input_context.py"]
    n7["backend/tests/test_profile_capacity.py"]
    n8["backend/tests/test_task_discussion.py"]
    n0 --> n3
    n0 --> n5
    n1 --> n0
    n2 --> n3
    n3 --> n1
    n4 --> n0
    n4 --> n3
    n5 --> n0
    n5 --> n3
    n6 --> n0
    n6 --> n3
    n6 --> n4
    n6 --> n5
    n7 --> n0
    n7 --> n1
    n7 --> n3
    n7 --> n4
    n8 --> n0
    n8 --> n3
    click n0 "../modules/commands.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/models_capacity.md"
    click n4 "../modules/capacity_service.md"
    click n5 "../modules/planning_input_context.md"
    click n6 "../modules/test_planning_input_context.md"
    click n7 "../modules/test_profile_capacity.md"
    click n8 "../modules/test_task_discussion.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [commands](../modules/commands.md) |
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [capacity_service](../modules/capacity_service.md) |
| Inbound | [planning_input_context](../modules/planning_input_context.md) |
| Inbound | [test_planning_input_context](../modules/test_planning_input_context.md) |
| Inbound | [test_profile_capacity](../modules/test_profile_capacity.md) |
| Inbound | [test_task_discussion](../modules/test_task_discussion.md) |
| Outbound | [app_database](../modules/app_database.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [PlanningState](../entities/PlanningState.md) | 11 | `Base` | — |
| [ProfileAvailability](../entities/ProfileAvailability.md) | 19 | `Base` | — |
| [ProfileAbsence](../entities/ProfileAbsence.md) | 30 | `Base` | — |
