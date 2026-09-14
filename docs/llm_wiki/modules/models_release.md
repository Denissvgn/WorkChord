# release Module

**Path:** `backend/app/models/release.py`

## Description

Release model for shipped-work tracking.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.models.external_link` | `ExternalLink` |
| `app.models.project` | `Project` |
| `app.models.task` | `Task` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `date`, `datetime` |
| `enum` | `Enum` |
| `sqlalchemy` | `CheckConstraint`, `Column`, `Date`, `ForeignKey`, `Index`, `Integer`, `String`, `Table`, `Text`, `and_` |
| `sqlalchemy.orm` | `Mapped`, `foreign`, `mapped_column`, `relationship` |
| `typing` | `TYPE_CHECKING`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/external_link.py"]
    n3["backend/app/models/project.py"]
    n4["backend/app/models/release.py"]
    n5["backend/app/models/task.py"]
    n6["backend/app/services/release_service.py"]
    n7["backend/app/utils/time.py"]
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n2 --> n0
    n2 --> n7
    n3 --> n0
    n3 --> n4
    n3 --> n5
    n3 --> n7
    n4 --> n0
    n4 --> n2
    n4 --> n3
    n4 --> n5
    n4 --> n7
    n5 --> n0
    n5 --> n2
    n5 --> n3
    n5 --> n7
    n6 --> n3
    n6 --> n4
    n6 --> n5
    n6 --> n7
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_external_link.md"
    click n3 "../modules/models_project.md"
    click n4 "../modules/models_release.md"
    click n5 "../modules/models_task.md"
    click n6 "../modules/release_service.md"
    click n7 "../modules/time.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [models_project](../modules/models_project.md) |
| Inbound | [release_service](../modules/release_service.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [models_external_link](../modules/models_external_link.md) |
| Outbound | [models_project](../modules/models_project.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ReleaseStatus](../entities/models_release_ReleaseStatus.md) | Enum | 29 | `str`, `Enum` | Release lifecycle independent of task status. |
| [Release](../entities/models_release_Release.md) | Class | 60 | `Base` | Lightweight shipping record scoped to one project. |
