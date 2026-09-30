# PlanningState

**Location:** `backend/app/models/capacity.py:11`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_capacity](../modules/models_capacity.md)

## Description

Lazy singleton used to serialize shared planning before iteration and task reservations. Each command reserves one revision; preview and failure roll back that reservation with domain changes. This is a coarse workspace serialization boundary, not a global scheduling optimizer.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True)` | — |
| `revision` | `Mapped[int]` | `mapped_column(Integer, nullable=False, default=0)` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["PlanningState (backend/app/models/capacity.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/commands.py"]
    n3["backend/app/models/__init__.py"]
    n4["backend/app/services/capacity_service.py"]
    n5["backend/tests/test_profile_capacity.py"]
    n6["backend/tests/test_task_discussion.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/models_capacity.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/commands.md"
    click n3 "../modules/models___init__.md"
    click n4 "../modules/capacity_service.md"
    click n5 "../modules/test_profile_capacity.md"
    click n6 "../modules/test_task_discussion.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_capacity](../modules/models_capacity.md) | 0 | `id`, `revision` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `commands` | import | [commands](../modules/commands.md) | — |
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `capacity_service` | import | [capacity_service](../modules/capacity_service.md) | — |
| `test_profile_capacity` | import | [test_profile_capacity](../modules/test_profile_capacity.md) | — |
| `test_task_discussion` | import | [test_task_discussion](../modules/test_task_discussion.md) | — |
