# label Module

**Path:** `backend/app/models/label.py`

## Description

Governed label taxonomy models.

## Imports

| Source | Symbols |
|--------|---------|
| `app.database` | `Base` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `datetime` | `datetime` |
| `sqlalchemy` | `Boolean`, `ForeignKey`, `Integer`, `String`, `Text`, `UniqueConstraint` |
| `sqlalchemy.orm` | `Mapped`, `mapped_column`, `relationship` |
| `typing` | `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/database.py"]
    n1["backend/app/models/__init__.py"]
    n2["backend/app/models/label.py"]
    n3["backend/app/services/agent_service.py"]
    n4["backend/app/services/label_service.py"]
    n5["backend/app/services/triage_service.py"]
    n6["backend/app/utils/time.py"]
    n1 --> n2
    n2 --> n0
    n2 --> n6
    n3 --> n2
    n3 --> n6
    n4 --> n2
    n5 --> n2
    n5 --> n6
    click n0 "../modules/app_database.md"
    click n1 "../modules/models___init__.md"
    click n2 "../modules/models_label.md"
    click n3 "../modules/agent_service.md"
    click n4 "../modules/label_service.md"
    click n5 "../modules/triage_service.md"
    click n6 "../modules/time.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [models___init__](../modules/models___init__.md) |
| Inbound | [agent_service](../modules/agent_service.md) |
| Inbound | [label_service](../modules/label_service.md) |
| Inbound | [triage_service](../modules/triage_service.md) |
| Outbound | [app_database](../modules/app_database.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [LabelGroup](../entities/models_label_LabelGroup.md) | 12 | `Base` | A governed group for related task label slugs. |
| [Label](../entities/models_label_Label.md) | 44 | `Base` | A governed label slug compatible with existing task tag strings. |
