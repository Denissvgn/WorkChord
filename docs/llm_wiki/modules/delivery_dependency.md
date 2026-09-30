# delivery_dependency Module

**Path:** `backend/app/models/delivery_dependency.py`

## Description

Persists exactly one task or milestone prerequisite per delivery edge. Foreign-key restrictions protect referenced targets. Flush hooks collect relevant changes for the owning command’s global cycle validation and downstream invalidation; they do not independently commit.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.models.project` | `ProjectMilestone` |
| `app.models.task` | `Task`, `TaskDependency` |
| `sqlalchemy` | `CheckConstraint`, `ForeignKey`, `Integer`, `UniqueConstraint`, `event`, `inspect` |
| `sqlalchemy.orm` | `Mapped`, `Session`, `mapped_column` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/delivery_dependency.py"]
    n3["backend/app/models/project.py"]
    n4["backend/app/models/task.py"]
    n5["backend/app/services/delivery_dependency_service.py"]
    n6["backend/tests/database_migration/test_postgresql_transfer.py"]
    n7["backend/tests/test_delivery_dependencies.py"]
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n2 --> n0
    n2 --> n3
    n2 --> n4
    n3 --> n0
    n3 --> n4
    n4 --> n0
    n4 --> n3
    n5 --> n2
    n5 --> n3
    n5 --> n4
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n7 --> n2
    n7 --> n3
    n7 --> n4
    n7 --> n5
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/delivery_dependency.md"
    click n3 "../modules/models_project.md"
    click n4 "../modules/models_task.md"
    click n5 "../modules/delivery_dependency_service.md"
    click n6 "../modules/test_postgresql_transfer.md"
    click n7 "../modules/test_delivery_dependencies.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [delivery_dependency_service](../modules/delivery_dependency_service.md) |
| Inbound | [test_postgresql_transfer](../modules/test_postgresql_transfer.md) |
| Inbound | [test_delivery_dependencies](../modules/test_delivery_dependencies.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [models_project](../modules/models_project.md) |
| Outbound | [models_task](../modules/models_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [DeliveryDependency](../entities/DeliveryDependency.md) | 9 | `Base` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `track_delivery_changes` | `(session, _flush_context, _instances)` | `@event.listens_for(Session, 'before_flush')` | Collect changes for transactional downstream invalidation without rewriting history. |
