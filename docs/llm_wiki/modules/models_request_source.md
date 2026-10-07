# request_source Module

**Path:** `backend/app/models/request_source.py`

## Description

Request source models for customer and intake traceability.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.models.triage` | `TriageItem` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `datetime` |
| `enum` | `Enum` |
| `sqlalchemy` | `CheckConstraint`, `ForeignKey`, `Index`, `Integer`, `String`, `Text`, `UniqueConstraint` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column`, `relationship` |
| `typing` | `Optional`, `TYPE_CHECKING` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/project.py"]
    n3["backend/app/models/request_source.py"]
    n4["backend/app/models/task.py"]
    n5["backend/app/models/triage.py"]
    n6["backend/app/services/request_source_service.py"]
    n7["backend/app/services/task_hierarchy_service.py"]
    n8["backend/app/services/task_service.py"]
    n9["backend/app/utils/time.py"]
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n2 --> n0
    n2 --> n3
    n2 --> n4
    n2 --> n9
    n3 --> n0
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n3 --> n9
    n4 --> n0
    n4 --> n2
    n4 --> n3
    n4 --> n9
    n5 --> n0
    n5 --> n2
    n5 --> n3
    n5 --> n4
    n5 --> n9
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n6 --> n5
    n7 --> n3
    n7 --> n4
    n8 --> n2
    n8 --> n3
    n8 --> n4
    n8 --> n5
    n8 --> n7
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_project.md"
    click n3 "../modules/models_request_source.md"
    click n4 "../modules/models_task.md"
    click n5 "../modules/models_triage.md"
    click n6 "../modules/request_source_service.md"
    click n7 "../modules/task_hierarchy_service.md"
    click n8 "../modules/task_service.md"
    click n9 "../modules/time.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [models_project](../modules/models_project.md) |
| Inbound | [models_task](../modules/models_task.md) |
| Inbound | [models_triage](../modules/models_triage.md) |
| Inbound | [request_source_service](../modules/request_source_service.md) |
| Inbound | [task_hierarchy_service](../modules/task_hierarchy_service.md) |
| Inbound | [task_service](../modules/task_service.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [models_project](../modules/models_project.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [models_triage](../modules/models_triage.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [RequestSourceType](../entities/models_request_source_RequestSourceType.md) | Enum | 26 | `str`, `Enum` | Supported lightweight request intake source types. |
| [RequestSource](../entities/models_request_source_RequestSource.md) | Class | 37 | `Base` | Free-text source record that can be linked to work entities. |
| [RequestSourceLink](../entities/models_request_source_RequestSourceLink.md) | Class | 76 | `Base` | Link from one request source to exactly one supported target. |
