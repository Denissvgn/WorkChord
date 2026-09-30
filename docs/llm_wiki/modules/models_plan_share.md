# plan_share Module

**Path:** `backend/app/models/plan_share.py`

## Description

Immutable read-only plan snapshots shared through revocable links.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.models.iteration` | `Iteration` |
| `app.models.user_session` | `UserSession` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `datetime` |
| `sqlalchemy` | `ForeignKey`, `Index`, `Integer`, `JSON`, `String` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column`, `relationship` |
| `typing` | `TYPE_CHECKING`, `Any` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/iteration.py"]
    n3["backend/app/models/plan_share.py"]
    n4["backend/app/models/user_session.py"]
    n5["backend/app/services/plan_share_service.py"]
    n6["backend/app/utils/time.py"]
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n2 --> n0
    n2 --> n3
    n3 --> n0
    n3 --> n2
    n3 --> n4
    n3 --> n6
    n4 --> n0
    n4 --> n3
    n4 --> n6
    n5 --> n3
    n5 --> n4
    n5 --> n6
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_iteration.md"
    click n3 "../modules/models_plan_share.md"
    click n4 "../modules/user_session.md"
    click n5 "../modules/plan_share_service.md"
    click n6 "../modules/time.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [models_iteration](../modules/models_iteration.md) |
| Inbound | [user_session](../modules/user_session.md) |
| Inbound | [plan_share_service](../modules/plan_share_service.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [models_iteration](../modules/models_iteration.md) |
| Outbound | [user_session](../modules/user_session.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [PlanShare](../entities/models_plan_share_PlanShare.md) | 17 | `Base` | One immutable iteration plan snapshot owned by a browser session. |
